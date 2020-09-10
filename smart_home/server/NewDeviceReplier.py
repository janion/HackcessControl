from socket import *
from threading import Thread

import smart_home.common.Constants as Constants
import smart_home.common.NetworkUtilities as NetworkUtilities


class NewDeviceReplier:

    def __init__(self, client_list):
        self.client_list = client_list
        self.thread = Thread(target=self.listen_for_new_clients, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def listen_for_new_clients(self):
        while True:
            # Listen for UDP broadcasts of client IP addresses
            print("Listening for new clients")
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(('0.0.0.0', Constants.UDP_PORT_NUMBER))
            data = s.recv(256).decode()
            s.close()
            ip = NetworkUtilities.extract_ip_address(data)
            print("Client connected from", ip)
            self.client_list.add_client("<NAME>", ip)

            # Send server IP address to client IP address
            print("Sending connection details to client")
            s2 = socket()
            addr = getaddrinfo(ip, Constants.SERVER_CONNECTION_PORT_NUMBER)[0][-1]
            s2.connect(addr)
            s2.send(str.encode(Constants.IP_FORMAT % gethostbyname(gethostname())))
            s2.close()
