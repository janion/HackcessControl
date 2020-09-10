import sys

from smart_home.client.connections.NewDeviceAnnouncer import NewDeviceAnnouncer
from smart_home.client.connections.ServerPoller import ServerPoller
import smart_home.common.Constants as Constants


class Callback:

    def __init__(self):
        self.called = False

    def run(self, arg):
        # sys.stdout.write("\r%s" % arg)
        # sys.stdout.flush()
        print(arg)
        self.called = True

    def is_called(self):
        return self.called


class Client:

    DEFAULT_CLIENT_NAME = "CLIENT_DEVICE"

    def __init__(self, name=DEFAULT_CLIENT_NAME):
        self.name = name
        self.server_ip = "Not yet connected"

    def start(self):
        announcer = NewDeviceAnnouncer()
        self.server_ip, self.name = announcer.connect_to_server(self.name)

        server_poller = ServerPoller(self.server_ip)
        server_poller.start()

        callback = None

        while True:
            # Do useful things
            # Recording data, informing server, polling server, etc.

            if callback is None or callback.is_called():
                callback = Callback()
                server_poller.add_request(Constants.JSON_TIME, lambda data: callback.run(data[Constants.JSON_TIME]))

if __name__ == "__main__":
    client = Client()
    client.start()
