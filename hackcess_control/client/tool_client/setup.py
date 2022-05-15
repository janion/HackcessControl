import os


def do_setup():
    os.mkdir("hackcess_control")
    os.mkdir("hackcess_control/common")
    os.mkdir("hackcess_control/client")
    os.mkdir("hackcess_control/client/connections")
    os.mkdir("hackcess_control/client/implementations")
    os.mkdir("hackcess_control/client/implementations/example")
    os.mkdir("hackcess_control/client/implementations/example/esp8266")
    os.mkdir("hackcess_control/client/implementations/example/esp8266/tool_client")

    os.rename("Constants.py", "hackcess_control/common/Constants.py")
    os.rename("Client.py", "hackcess_control/client/Client.py")
    os.rename("NewDeviceAnnouncer.py", "hackcess_control/client/connections/NewDeviceAnnouncer.py")
    os.rename("ServerConnection.py", "hackcess_control/client/connections/ServerConnection.py")
    os.rename("PushButtonUpdatingClient.py", "hackcess_control/client/implementations/example/esp8266/tool_client/PushButtonUpdatingClient.py")

    os.remove("setup.py")
