import time

from smart_home.client_implementations.example import EpochTimePollingClient


class EpochTimeUpdatingClient(EpochTimePollingClient):

    def __init__(self):
        super().__init__("EpochTimeUpdater", fields=[(self.FIELD_NAME, 0)])
        self.last_local_time = 0

    def process(self, server_connection):
        super().process(server_connection)
        client_time = int(time.time())
        if client_time != self.last_local_time:
            server_connection.update_field(self.FIELD_NAME, client_time)


if __name__ == "__main__":
    client = EpochTimeUpdatingClient()
    client.start()
