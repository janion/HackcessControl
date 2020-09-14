import sys
import time

from smart_home.client.connections.NewDeviceAnnouncer import NewDeviceAnnouncer
# from smart_home.client.connections.ServerPoller import ServerPoller
from smart_home.client.connections.ServerConnection import ServerConnection
import smart_home.common.Constants as Constants


# class Callback:
#
#     def __init__(self):
#         self.called = False
#
#     def run(self, arg):
#         # sys.stdout.write("\r%s" % arg)
#         # sys.stdout.flush()
#         print(arg)
#         self.called = True
#
#     def is_called(self):
#         return self.called


class Client:

    DEFAULT_CLIENT_NAME = "CLIENT_DEVICE"

    def __init__(self, name=DEFAULT_CLIENT_NAME):
        self.name = name
        self.server_ip = "Not yet connected"

    def start(self):
        announcer = NewDeviceAnnouncer()
        self.server_ip, self.name = announcer.connect_to_server(self.name)

        server_connection = ServerConnection(self.server_ip)

        # last_time = ""
        # while True:
        #     result = server_connection.poll(Constants.JSON_TIME)
        #
        #     server_time = result[Constants.JSON_TIME]
        #     if server_time != last_time:
        #         sys.stdout.write("\r%s" % server_time)
        #         sys.stdout.flush()
        #         last_time = server_time

        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])

        client_time_field = "client_time"
        last_local_time = int(time.time())
        server_connection.install_field(client_time_field, last_local_time)

        poll_period = 5
        last_poll_time = 0;

        last_remote_time = 0
        while True:
            client_time = int(time.time())
            if client_time != last_local_time:
                server_connection.update_field(client_time_field, client_time)
                last_local_time = client_time

            if client_time > last_poll_time + poll_period:
                result = server_connection.poll(client_time_field)

                remote_time = result[client_time_field]
                if remote_time != last_remote_time:
                    sys.stdout.write("\r%s" % remote_time)
                    sys.stdout.flush()
                    last_remote_time = remote_time

                last_poll_time = client_time

if __name__ == "__main__":
    client = Client()
    client.start()
