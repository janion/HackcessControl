import sys
if sys.implementation.name == "cpython":
    import json
    from socket import *
elif sys.implementation.name == "micropython":
    import ujson as json
    from usocket import *
    import network

import os
import json

import hackcess_control.common.Constants as Constants


class NewDeviceAnnouncer:

    def connect_to_server(self, name):
        response = None
        existing_name = self._find_existing_name_file(name)
        if existing_name is not None:
            client_name = existing_name
        else:
            client_name = name
        while response is None:
            self._anounce_ip_to_server(client_name)
            response = self._await_server_response(name)

        return response

    def _find_existing_name_file(self, desired_name):
        if Constants.DEVICE_NAME_FILE in os.listdir():
            with open(Constants.DEVICE_NAME_FILE, "r") as name_file:
                json_data = json.loads(name_file.read())

            if desired_name in json_data.keys():
                return json_data[desired_name]
            elif Constants.JSON_CLIENT_NAME in json_data.keys():
                return json_data[Constants.JSON_CLIENT_NAME]
        return None

    def _anounce_ip_to_server(self, name):
        # Send UDP broadcast to give IP address to server
        print("Requesting server connection")
        cs = socket(AF_INET, SOCK_DGRAM)
        if sys.implementation.name == "cpython":
            cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto(str.encode(self._create_json(name)), ('255.255.255.255', Constants.UDP_PORT_NUMBER))
        cs.close()

    def _create_json(self, name):
        data = {Constants.JSON_MESSAGE_TYPE: Constants.JSON_MESSAGE_TYPE_ANNOUNCE_CLIENT,
                Constants.JSON_IP_ADDRESS: self._get_ip_address(),
                Constants.JSON_CLIENT_NAME: name}
        return json.dumps(data)

    def _get_ip_address(self):
        if sys.implementation.name == "cpython":
            return gethostbyname(gethostname() + ".local")
        elif sys.implementation.name == "micropython":
            return network.WLAN(network.STA_IF).ifconfig()[0]

    def _await_server_response(self, desired_name):
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

        json_data = json.loads(data)
        ip = json_data[Constants.JSON_IP_ADDRESS]
        assigned_name = json_data[Constants.JSON_CLIENT_NAME]
        print('Server connected from %s with client name: %s' % (ip, assigned_name))

        self._write_name_file(desired_name, assigned_name)
        return ip, assigned_name

    def _write_name_file(self, desired_name, assigned_name):
        if Constants.DEVICE_NAME_FILE in os.listdir():
            with open(Constants.DEVICE_NAME_FILE, "r") as name_file:
                json_data = json.loads(name_file.read())
        else:
            json_data = {}

        if desired_name not in json_data.keys():
            json_data[desired_name] = assigned_name
            with open(Constants.DEVICE_NAME_FILE, "w") as name_file:
                name_file.write(json.dumps(json_data))
