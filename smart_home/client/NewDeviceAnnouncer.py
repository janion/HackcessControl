import select
from socket import *

import smart_home.common.Constants as Constants
import smart_home.common.NetworkUtilities as NetworkUtilities


class NewDeviceAnnouncer:

    def connect_to_server(self):
        response = None
        while response is None:
            self._anounce_ip_to_server()
            response = self._await_server_response()

        return response

    def _anounce_ip_to_server(self):
        # Send UDP broadcast to give IP address to server
        print("Requesting server connection")
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto(str.encode(Constants.IP_FORMAT % gethostbyname(gethostname())), ('255.255.255.255', Constants.UDP_PORT_NUMBER))
        cs.close()

    def _await_server_response(self):
        try:
            # Await the server to give its IP address
            addr = getaddrinfo('0.0.0.0', Constants.SERVER_CONNECTION_PORT_NUMBER)[0][-1]

            s = socket()
            s.settimeout(10)
            s.bind(addr)
            s.listen(1)

            print('Awaiting server response')

            cl, connected_addr = s.accept()
            data = cl.recv(256).decode()
            cl.close()

            ip = NetworkUtilities.extract_ip_address(data)
            print('Server connected from', ip)

            return ip
        except timeout:
            pass
