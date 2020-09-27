import os


def do_setup():
    os.mkdir("smart_home")
    os.mkdir("smart_home/common")
    os.mkdir("smart_home/client")
    os.mkdir("smart_home/client/connections")
    os.mkdir("smart_home/client/implementations")
    os.mkdir("smart_home/client/implementations/example")
    os.mkdir("smart_home/client/implementations/example/esp8266")
    os.mkdir("smart_home/client/implementations/example/esp8266/button")

    os.rename("Constants.py", "smart_home/common/Constants.py")
    os.rename("Client.py", "smart_home/client/Client.py")
    os.rename("NewDeviceAnnouncer.py", "smart_home/client/connections/NewDeviceAnnouncer.py")
    os.rename("ServerConnection.py", "smart_home/client/connections/ServerConnection.py")
    os.rename("PushButtonUpdatingClient.py", "smart_home/client/implementations/example/esp8266/button/PushButtonUpdatingClient.py")

    os.remove("setup.py")
