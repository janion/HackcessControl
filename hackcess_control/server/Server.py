import time

import hackcess_control.common.Constants as Constants
from hackcess_control.server.connections.ClientList import ClientList
from hackcess_control.server.connections.NewDeviceReplier import NewDeviceReplier
from hackcess_control.server.data.Database import Database
from hackcess_control.server.connections.Interface import Interface


class Server:

    def __init__(self):
        self.database = Database();
        self.database.add_user_permission(Constants.JSON_TIME, Constants.SERVER_ONLY_IP, time.strftime("%H:%M:%S"))

    def start(self):
        client_list = ClientList()
        client_list.add_client_added_callback(lambda client_id: print("Callback for IP %s (%s)" % (client_id.get_ip(), client_id.get_id())))
        replier = NewDeviceReplier(client_list)
        replier.start()
        interface = Interface(client_list, self.database)
        interface.start()

        last_time = ""
        while True:
            # Do useful things
            # Listening for connections, serving clients, storing data, etc.

            current_time = time.strftime(Constants.JSON_TIME_FORMAT)
            if current_time != last_time:
                self.database.set_field_value(Constants.JSON_TIME, current_time, Constants.SERVER_ONLY_IP)
                last_time = current_time

            time.sleep(1)


if __name__ == "__main__":
    server = Server()
    server.start()
