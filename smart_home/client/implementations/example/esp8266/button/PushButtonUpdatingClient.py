import utime as time
from machine import Pin

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


class PushButtonUpdatingClient(Client):

    FIELD_NAME = "esp8266_button"
    PRESS_TIME_INTERVAL = 1

    def __init__(self):
        super().__init__("esp8266_button_updater")
        self.button = Pin(5, Pin.IN)
        self.last_press = time.time()

    def setup_process(self, server_connection):
        print("Server Time: %s" % server_connection.poll(Constants.JSON_TIME)[Constants.JSON_TIME])
        server_connection.install_field(self.FIELD_NAME, self.button.value())

    def process(self, server_connection):
        if self.button.value() and time.time() > self.last_press + self.PRESS_TIME_INTERVAL:
            server_connection.update_field(self.FIELD_NAME, self.button.value())
            self.last_press = time.time()
        time.sleep(0.1)
