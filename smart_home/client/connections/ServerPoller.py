import socket
import json
from threading import Thread
import smart_home.common.Constants as Constants


class ServerPoller:

    def __init__(self, server_ip):
        self.requests = []
        self.server_ip = server_ip

        self.thread = Thread(target=self._poll_server, daemon=True)

    def add_request(self, dataType, callback):
        self.requests.append((dataType, callback))

    def start(self):
        self.thread.start()

    def _poll_server(self):
        s = socket.socket()
        addr = socket.getaddrinfo(self.server_ip, Constants.CLIENT_CONNECTION_PORT_NUMBER)[0][-1]
        s.connect(addr)
        while True:
            if len(self.requests) > 0:
                data_type, callback = self.requests.pop(0)
                s.send(str.encode(self._create_json(data_type)))
                data = s.recv(1024).decode()
                callback(json.loads(data))

        s.close()

    def _create_json(self, data_type):
        data = {Constants.JSON_MESSAGE_TYPE: Constants.JSON_MESSAGE_TYPE_POLL,
                Constants.JSON_DATA_TYPE: data_type}
        return json.dumps(data)
