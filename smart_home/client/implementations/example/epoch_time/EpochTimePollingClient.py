import sys
import time

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


class EpochTimePollingClient(Client):

    POLL_PERIOD = 5
    FIELD_NAME = "client_time"

    def __init__(self, name="EpochTimePoller"):
        super().__init__(name)

        self.last_poll_time = 0
        self.last_local_time = 0
        self.last_remote_time = 0

    def setup_process(self, server_connection):
        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])
        self.last_local_time = int(time.time())

    def process(self, server_connection):
        if int(time.time()) > self.last_poll_time + self.POLL_PERIOD:
            result = server_connection.poll(self.FIELD_NAME)

            remote_time = result[self.FIELD_NAME]
            if remote_time != self.last_remote_time:
                sys.stdout.write("\r%s" % remote_time)
                sys.stdout.flush()
                self.last_remote_time = remote_time

            self.last_poll_time = int(time.time())
        time.sleep(1)


if __name__ == "__main__":
    client = EpochTimePollingClient()
    client.start()
