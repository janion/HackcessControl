import os
import ujson as json
from machine import Pin
import network

from CaptivePortal import CaptivePortal


CREDENTIALS_FILE = "wifi.json"
SSID = "ssid"
PWD = "pwd"


class Connection:

    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        network.WLAN(network.AP_IF).active(False)
        self.hasBeenConnected = self.sta_if.isconnected()
        self.statusLed = Pin(2, Pin.OUT)
        self.inverted = os.uname().sysname == "esp8266"
        self.updateLed()

    def updateLed(self):
        if not self.sta_if.isconnected():
            self.statusLed.value(not self.inverted)
        else:
            self.statusLed.value(self.inverted)

    def checkOrMakeConnection(self):
        if not self.sta_if.isconnected():
            if self.hasBeenConnected:
                print("Disconnect detected")
            print("Reading credentials")

            credentials = self._read_credentials()
            if credentials is not None:
                ssid = credentials[SSID]
                password = credentials[PWD]

                print("Connecting to network:", ssid)
                self.sta_if.connect(ssid, password)
                while not self.sta_if.isconnected():
                    if self.sta_if.status() in [network.STAT_WRONG_PASSWORD, network.STAT_NO_AP_FOUND, network.STAT_CONNECT_FAIL, network.STAT_IDLE]:
                        break;
                if self.sta_if.isconnected():
                    self.hasBeenConnected = True
                    print("Network config:", self.sta_if.ifconfig())
                    self.updateLed()
                    return

            self.sta_if.active(False)
            captive_portal = CaptivePortal()
            captive_portal.start()

    def _read_credentials(self):
        if CREDENTIALS_FILE in os.listdir():
            with open(CREDENTIALS_FILE, "r") as json_file:
                return json.loads(json_file.read())
        return None
