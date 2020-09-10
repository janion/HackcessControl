import time

import smart_home.common.Constants as Constants
from smart_home.server.connections.ClientList import ClientList
from smart_home.server.connections.NewDeviceReplier import NewDeviceReplier
from smart_home.server.data.Database import Database
from smart_home.server.connections.Interface import Interface


class Server:

    def __init__(self):
        self.database = Database();
        self.database.add_field(Constants.JSON_TIME, Constants.SERVER_ONLY_IP, time.strftime("%H:%M:%S"))

    def start(self):
        client_list = ClientList()
        client_list.add_client_added_callback(lambda client_id: print("Callback for IP %s (%s)" % (client_id.get_ip(), client_id.get_name())))
        replier = NewDeviceReplier(client_list)
        replier.start()
        interface = Interface(client_list, self.database)
        interface.start()

        while True:
            # Do useful things
            # Listening for connections, serving clients, storing data, etc.
            self.database.set_field_value(Constants.JSON_TIME, Constants.SERVER_ONLY_IP, time.strftime(Constants.JSON_TIME_FORMAT))

if __name__ == "__main__":
    server = Server()
    server.start()
