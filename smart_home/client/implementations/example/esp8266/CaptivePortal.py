import usocket as socket
import utime as time
import ujson as json
import network
import machine


class CaptivePortal:

    class DNSQuery:
        def __init__(self, data):
            self.data = data
            self.domain = ''

            print("Reading datagram data...")
            m = data[2]  # ord(data[2])
            type = (m >> 3) & 15  # Opcode bits
            if type == 0:  # Standard query
                start = 12
                lon = data[start]  # ord(data[start])
                while lon != 0:
                    self.domain += data[start + 1:start + lon + 1].decode("utf-8") + '.'
                    start += lon + 1
                    lon = data[start]  # ord(data[start])

        def reply(self, ip):
            packet = b''
            print("Reply {} == {}".format(self.domain, ip))
            if self.domain:
                packet += self.data[:2] + b"\x81\x80"
                packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'  # Questions and Answers Counts
                packet += self.data[12:]  # Original Domain Name Question
                packet += b'\xc0\x0c'  # Pointer to domain name
                packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
                packet += bytes(map(int, ip.split('.')))  # 4 bytes of IP
            return packet

    CONTENT = b"""\
    HTTP/1.0 200 OK

    <!doctype html>
    <html>
        <head>
            <title>Wifi Login</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta charset="utf8">
        </head>
        <body>
            <h1>Set Wifi Credentials</h1>
            <form action="/connect">
                SSID: <input type="text" name="ssid" required><br>
                Password: <input type="text" name="pwd" required><br>
                <input type="submit" value="Connect">
            </form>
        </body>
    </html>
    """

    CREDENTIALS_FILE = "wifi.json"
    SSID = "ssid"
    PWD = "pwd"

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid="Connect_to_wifi", password="bananabanana", authmode=4)  # authmode=1 == no pass

    def start(self):
        # DNS Server
        ip = self.ap.ifconfig()[0]
        print('DNS Server: dom.query. 60 IN A {:s}'.format(ip))

        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.bind(('', 53))

        # Web Server
        s = socket.socket()
        ai = socket.getaddrinfo(ip, 80)
        print("Web Server: Bind address info:", ai)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        s.settimeout(2)
        print("Web Server: Listening http://{}:80/".format(ip))

        try:
            while 1:

                # DNS Loop
                print("Checking DNS")
                try:
                    data, addr = udps.recvfrom(1024)
                    print("Incomming datagram")
                    p = self.DNSQuery(data)
                    udps.sendto(p.reply(ip), addr)
                    print('Replying: {:s} -> {:s}'.format(p.domain, ip))
                except:
                    print("No datagram")

                # Web loop
                print("Checking webpage requests")
                try:
                    res = s.accept()
                    client_sock = res[0]

                    client_stream = client_sock

                    print("Request:")
                    req = client_stream.readline()
                    print(req)
                    while True:
                        h = client_stream.readline()
                        if h == b"" or h == b"\r\n" or h == None:
                            break
                        print(h)

                    request_url = req[8:-11]
                    if request_url.startswith('/connect?'):
                        params = request_url[9:]
                        try:
                            credentials = {key: value for (key, value) in [x.split(b'=') for x in params.split(b'&')]}
                        except:
                            credentials = {}

                        if self.SSID in credentials.keys() and self.PWD in credentials.keys():
                            json_map = {self.SSID: credentials[self.SSID],
                                        self.PWD: credentials[self.PWD]}
                            json_data = json.dumps(json_map, indent=4)
                            with open(self.CREDENTIALS_FILE, "w") as json_file:
                                json_file.write(json_data)
                            machine.reset()
                    else:
                        client_stream.write(self.CONTENT)
                        client_stream.close()
                except:
                    print("timeout for web... moving on...")
                print("loop")
                time.sleep(0.3)
        except KeyboardInterrupt:
            print('Closing')
        udps.close()
