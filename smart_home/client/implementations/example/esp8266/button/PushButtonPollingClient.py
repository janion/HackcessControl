import sys
import time

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants
from smart_home.client.implementations.example.esp8266.button.PushButtonUpdatingClient import FIELD_NAME


class PushButtonPollingClient(Client):

    POLL_PERIOD = 1

    def __init__(self):
        super().__init__("esp8266_button_poller")

        self.last_poll_time = 0
        self.last_button_state = 0

    def setup_process(self, server_connection):
        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])

    def process(self, server_connection):
        if int(time.time()) > self.last_poll_time + self.POLL_PERIOD:
            result = server_connection.poll(FIELD_NAME)

            button_state = result[FIELD_NAME]
            if button_state != Constants.NO_DATA:
                update_time = result[Constants.JSON_UPDATE_TIMESTAMP]
                if button_state != self.last_button_state:
                    if button_state:
                        sys.stdout.write("\rButton pressed at %s" % update_time)
                    else:
                        sys.stdout.write("\rButton released at %s" % update_time)
                    sys.stdout.flush()
                    self.last_button_state = button_state

            self.last_poll_time = int(time.time())
        time.sleep(0.1)


if __name__ == "__main__":
    client = PushButtonPollingClient()
    client.start()
