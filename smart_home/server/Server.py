import time

import smart_home.common.Constants as Constants
from smart_home.server.NewDeviceReplier import NewDeviceReplier
from smart_home.server.connections.ClientList import ClientList
from smart_home.server.data.Database import Database


class Server:

    def __init__(self):
        self.database = Database();
        self.database.add_field("ClockTime", Constants.SERVER_ONLY_IP, time.strftime("%H:%M:%S"))

    def start(self):
        client_list = ClientList()
        client_list.add_client_added_callback(lambda client_id: print("Callback for IP %s (%s)" % (client_id.get_ip(), client_id.get_name())))
        replier = NewDeviceReplier(client_list)
        replier.start()

        while True:
            # Do useful things
            # Listening for connections, serving clients, storing data, etc.
            self.database.set_field_value("ClockTime", Constants.SERVER_ONLY_IP, time.strftime("%H:%M:%S"))

if __name__ == "__main__":
    server = Server()
    server.start()
