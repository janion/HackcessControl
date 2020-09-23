import sys
if sys.implementation.name == "micropython":
    import utime as time
    from machine import Pin

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


FIELD_NAME = "esp8266_button"


class PushButtonUpdatingClient(Client):

    PRESS_TIME_INTERVAL = 1

    def __init__(self):
        super().__init__("esp8266_button_updater", [(FIELD_NAME, 0)])
        self.button = Pin(5, Pin.IN, Pin.PULL_UP)
        self.last_state_change = time.time()
        self.last_button_state = 1 - self.button.value()

    def setup_process(self, server_connection):
        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])

    def process(self, server_connection):
        button_state = 1 - self.button.value()
        if (button_state != self.last_button_state and not button_state)\
                or (button_state != self.last_button_state and time.time() > self.last_state_change + self.PRESS_TIME_INTERVAL):
            server_connection.update_field(FIELD_NAME, button_state)
            self.last_button_state = button_state
            self.last_state_change = time.time()
        time.sleep(0.1)
