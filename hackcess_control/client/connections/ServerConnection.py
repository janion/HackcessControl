import sys
if sys.implementation.name == "cpython":
    import json
    import socket
elif sys.implementation.name == "micropython":
    import ujson as json
    import usocket as socket
import hackcess_control.common.Constants as Constants


class ServerConnection:

    def __init__(self, server_ip, client_name):
        self.server_ip = server_ip
        self.client_name = client_name

    def poll(self, user_id):
        return self._send_to_server(Constants.JSON_MESSAGE_TYPE_POLL, user_id)

    def install_user_permission(self, user_id):
        return self._send_to_server(Constants.JSON_MESSAGE_TYPE_INSTALL_USER, user_id)

    def _send_to_server(self, message_type, user_id):
        s = socket.socket()
        addr = socket.getaddrinfo(self.server_ip, Constants.CLIENT_CONNECTION_PORT_NUMBER)[0][-1]
        s.connect(addr)

        s.send(str.encode(self._create_json(message_type, user_id)))
        data = s.recv(1024).decode()
        s.close()

        return json.loads(data)

    def _create_json(self, message_type, user_id):
        data = {Constants.JSON_MESSAGE_TYPE: message_type,
                Constants.JSON_CLIENT_NAME: self.client_name,
                Constants.JSON_USER_ID: user_id}
        return json.dumps(data)
