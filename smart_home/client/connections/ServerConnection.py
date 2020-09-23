import sys
if sys.implementation.name == "cpython":
    import json
    import socket
elif sys.implementation.name == "micropython":
    import ujson as json
    import usocket as socket
import smart_home.common.Constants as Constants


class ServerConnection:

    def __init__(self, server_ip):
        self.server_ip = server_ip

    def poll(self, data_type, client_name):
        return self._send_to_server(Constants.JSON_MESSAGE_TYPE_POLL, data_type, client_name)

    def install_field(self, data_type, value, client_name):
        return self._send_to_server(Constants.JSON_MESSAGE_TYPE_INSTALL, data_type, client_name, value)
    
    def update_field(self, data_type, value, client_name):
        return self._send_to_server(Constants.JSON_MESSAGE_TYPE_UPDATE, data_type, client_name, value)

    def _send_to_server(self, message_type, data_type, client_name, value=None):
        s = socket.socket()
        addr = socket.getaddrinfo(self.server_ip, Constants.CLIENT_CONNECTION_PORT_NUMBER)[0][-1]
        s.connect(addr)

        s.send(str.encode(self._create_json(message_type, data_type, client_name, value)))
        data = s.recv(1024).decode()
        s.close()

        return json.loads(data)

    def _create_json(self, message_type, data_type, client_name, value=None):
        data = {Constants.JSON_MESSAGE_TYPE: message_type,
                Constants.JSON_CLIENT_NAME: client_name,
                Constants.JSON_DATA_TYPE: data_type}
        if value is not None:
            data[data_type] = value;
        return json.dumps(data)
