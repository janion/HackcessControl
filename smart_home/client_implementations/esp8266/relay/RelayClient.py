import utime as time
from machine import Pin

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


class RelayClient(Client):

    POLL_PERIOD = 5

    def __init__(self):
        super().__init__("esp8266_relay")
        self.relay = Pin(5, Pin.IN, Pin.PULL_UP)
        self.last_poll_time = 0

    def setup_process(self, server_connection):
        self.server_connection.install_field(self.name, Constants.OFF)

        time_update = server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME]
        print("Server Time: %s" % time_update[Constants.JSON_VALUE])

    def process(self, server_connection):
        if int(time.time()) - self.last_poll_time > self.POLL_PERIOD:
            result = server_connection.poll(self.name)

            button_state = result[self.name][Constants.JSON_VALUE]
            # These may not have to be inverted. I can't remember if that's the case for all GPIO pins
            if button_state == Constants.ON:
                self.relay.value(0)
            elif button_state == Constants.OFF:
                self.relay.value(1)
            self.last_poll_time = int(time.time())
        time.sleep(1)


if __name__ == "__main__":
    client = RelayClient()
    client.start()
