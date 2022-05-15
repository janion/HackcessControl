import sys
if sys.implementation.name == "micropython":
    import utime as time
    from machine import Pin
    import ujson as json
    import os

from hackcess_control.client.Client import Client
import hackcess_control.common.Constants as Constants


FIELD_NAME = "esp8266_button"


class RfidToolClient(Client):

    SCAN_TIME_INTERVAL = 1

    def __init__(self):
        super().__init__(RfidToolClient._get_device_name())
        self.rfid = None
        self.last_read = time.time()
        self.current_user = None
        self.relay = Pin(5, Pin.OUT)

    def process(self, server_connection):
        scanned_users = self.rfid.read()

        if self.current_user in scanned_users:
            return

        for user in scanned_users:
            result = server_connection.poll(user)
            is_permitted = result[Constants.JSON_USER_PERMISSION] != Constants.JSON_ACCESS_GRANTED
            if is_permitted:
                self.current_user = user
                # ESP8266 outputs are inverted
                self.relay.value(False)
                break

        time.sleep(self.SCAN_TIME_INTERVAL)

    @staticmethod
    def _get_device_name():
        if Constants.DEVICE_NAME_FILE in os.listdir():
            with open(Constants.DEVICE_NAME_FILE, "r") as name_file:
                json_data = json.loads(name_file.read())
                return json_data[Constants.JSON_CLIENT_NAME]
