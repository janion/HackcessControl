import network
import os
import ujson as json
from machine import Pin


class Connection():

    CREDENTIALS_FILE = "wifi.json"
    SSID = "ssid"
    PWD = "pwd"

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
            print("Scanning for networks...")

            credentials = self._read_credentials()
            ssid = credentials[self.SSID]
            password = credentials[self.PWD]

            networks = self.sta_if.scan()
            for network in networks:
                network_ssid = str(network[0])[2:-1]
                if network_ssid == ssid:
                    print("Connecting to network:", ssid)
                    self.sta_if.connect(ssid, password)
                    while not self.sta_if.isconnected():
                        pass
                    self.hasBeenConnected = True
                    print("Network config:", self.sta_if.ifconfig())
                    self.updateLed()
                    break

    def _read_credentials(self):
        if self.CREDENTIALS_FILE in os.listdir():
            with open(self.CREDENTIALS_FILE, "r") as json_file:
                return json.loads(json_file.read())
