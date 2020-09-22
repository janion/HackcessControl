from smart_home.client.connections.NewDeviceAnnouncer import NewDeviceAnnouncer
from smart_home.client.connections.ServerConnection import ServerConnection


class Client:

    DEFAULT_CLIENT_NAME = "CLIENT_DEVICE"

    def __init__(self, name=DEFAULT_CLIENT_NAME):
        self.name = name
        self.server_ip = "Not yet connected"
        self.announcer = NewDeviceAnnouncer()

    def start(self):
        self._connect_to_server()
        server_connection = ServerConnection(self.server_ip)

        self.setup_process(server_connection)

        while True:
            try:
                self.process(server_connection)
            except (TimeoutError, ConnectionResetError, ConnectionRefusedError):
                self._connect_to_server()

    def _connect_to_server(self):
        self.server_ip, self.name = self.announcer.connect_to_server(self.name)

    def setup_process(self, server_connection):
        pass

    def process(self, server_connection):
        raise NotImplementedError()
