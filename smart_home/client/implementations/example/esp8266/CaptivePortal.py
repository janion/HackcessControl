import usocket as socket
import utime as time
import ujson as json
import network
import machine
import re

import smart_home.common.Constants as Constants


# Based off existing code found here:
# https://github.com/amora-labs/micropython-captive-portal


class CaptivePortal:

    class DNSQuery:
        def __init__(self, data):
            self.data = data
            self.domain = ''

            m = data[2]
            _type = (m >> 3) & 15  # Opcode bits
            if _type == 0:  # Standard query
                start = 12
                lon = data[start]
                while lon != 0:
                    self.domain += data[start + 1:start + lon + 1].decode("utf-8") + '.'
                    start += lon + 1
                    lon = data[start]

        def reply(self, ip):
            packet = b''
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
            Device Name: <input type="text" name="name" required><br>
            <input type="submit" value="Connect">
        </form>
    </body>
</html>
"""

    SUCCESS = b"""\
HTTP/1.0 200 OK

<!doctype html>
<html>
    <head>
        <title>Wifi Login Success</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf8">
    </head>
    <body>
        <h1>Thanks!</h1>
        <h3>Connecting to wifi network...</h3>
    </body>
</html>
"""

    CREDENTIALS_REGEX = ".*/connect\\?ssid=(.*)&pwd=(.*)&name=(.*) .*\r\n"

    CREDENTIALS_FILE = "wifi.json"
    SSID = "ssid"
    PWD = "pwd"
    NAME = "name"

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid="Connect_to_wifi", authmode=1)

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
            while True:
                self._process_dns(udps, ip)
                self._process_web(s)
                time.sleep(0.3)
        except KeyboardInterrupt:
            print('Closing')
        udps.close()

    def _process_dns(self, udps, ip):
        try:
            data, addr = udps.recvfrom(1024)
            p = self.DNSQuery(data)
            udps.sendto(p.reply(ip), addr)
        except:
            pass

    def _process_web(self, s):
        try:
            res = s.accept()
            client_sock = res[0]
            client_stream = client_sock

            req = client_stream.readline()
            print(req)
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n" or h is None:
                    break
                    # print(h)

            match = re.match(self.CREDENTIALS_REGEX, req.decode())
            if match:
                client_stream.write(self.SUCCESS)
                client_stream.close()
                self._write_credentials_file(match.group(1), match.group(2))
                self._write_device_name_file(match.group(3))
                time.sleep(1)
                machine.reset()
            else:
                client_stream.write(self.CONTENT)
                client_stream.close()
        except:
            print("Timeout")

    def _write_credentials_file(self, ssid, pwd):
        json_map = {self.SSID: ssid,
                    self.PWD: pwd}
        json_data = json.dumps(json_map)
        with open(self.CREDENTIALS_FILE, "w") as json_file:
            json_file.write(json_data)

    def _write_device_name_file(self, name):
        json_map = {Constants.JSON_CLIENT_NAME: name}
        json_data = json.dumps(json_map)
        with open(Constants.DEVICE_NAME_FILE, "w") as json_file:
            json_file.write(json_data)
