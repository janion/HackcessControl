import sys
import time

from smart_home.client.connections.NewDeviceAnnouncer import NewDeviceAnnouncer
from smart_home.client.connections.ServerConnection import ServerConnection


class Client:

    DEFAULT_CLIENT_NAME = "CLIENT_DEVICE"

    def __init__(self, name=DEFAULT_CLIENT_NAME):
        self.name = name
        self.server_ip = "Not yet connected"

    def start(self):
        announcer = NewDeviceAnnouncer()
        self.server_ip, self.name = announcer.connect_to_server(self.name)

        server_connection = ServerConnection(self.server_ip)

        self.setup_process(server_connection)

        while True:
            self.process(server_connection)

    def setup_process(self, server_connection):
        pass

    def process(self, server_connection):
        raise NotImplementedError()


if __name__ == "__main__":
    client = Client()
    client.start()
