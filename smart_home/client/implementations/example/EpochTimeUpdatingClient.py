import sys
import time

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


class EpochTimeUpdatingClient(Client):

    POLL_PERIOD = 5
    FIELD_NAME = "client_time_example"

    def __init__(self):
        super().__init__("EpochTimeUpdater")

        self.last_poll_time = 0
        self.last_local_time = 0
        self.last_remote_time = 0

    def setup_process(self, server_connection):
        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])
        self.last_local_time = int(time.time())
        server_connection.install_field(self.FIELD_NAME, self.last_local_time)

    def process(self, server_connection):
        client_time = int(time.time())
        if client_time != self.last_local_time:
            server_connection.update_field(self.FIELD_NAME, client_time)

        if int(time.time()) > self.last_poll_time + self.POLL_PERIOD:
            result = server_connection.poll(self.FIELD_NAME)

            remote_time = result[self.FIELD_NAME]
            if remote_time != self.last_remote_time:
                sys.stdout.write("\r%s" % remote_time)
                sys.stdout.flush()
                self.last_remote_time = remote_time

            self.last_poll_time = int(time.time())


if __name__ == "__main__":
    client = EpochTimeUpdatingClient()
    client.start()
