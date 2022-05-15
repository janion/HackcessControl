import json
from socket import *
from threading import Thread

import hackcess_control.common.Constants as Constants


class NewDeviceReplier:

    def __init__(self, client_list):
        self.client_list = client_list
        self.thread = Thread(target=self._listen_for_new_clients, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def _listen_for_new_clients(self):
        while True:
            # Listen for UDP broadcasts of client IP addresses
            print("Listening for new clients")
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(('0.0.0.0', Constants.UDP_PORT_NUMBER))
            data = s.recv(256).decode()
            s.close()
            json_data = json.loads(data)
            ip = json_data[Constants.JSON_IP_ADDRESS]
            name = json_data[Constants.JSON_CLIENT_NAME]
            print("Client connected from", ip)

            original_name = name
            suffix = 1
            while not self.client_list.add_client(name, ip):
                name = "%s_%d" % (original_name, suffix)
                suffix += 1

            # Send server IP address to client IP address
            print("Sending connection details to client")
            s2 = socket()
            addr = getaddrinfo(ip, Constants.SERVER_CONNECTION_PORT_NUMBER)[0][-1]
            s2.connect(addr)
            s2.send(str.encode(self._create_json(name)))
            s2.close()

    def _create_json(self, name):
        data = {Constants.JSON_IP_ADDRESS: gethostbyname(gethostname()),
                Constants.JSON_CLIENT_NAME: name}
        return json.dumps(data)
