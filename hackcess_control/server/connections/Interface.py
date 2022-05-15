import socket
import json
from threading import Thread
from time import sleep

import hackcess_control.common.Constants as Constants


class Interface:

    def __init__(self, client_list, database):
        self.client_list = client_list
        self.database = database
        self.client_ips = []
        for id in self.client_list.get_client_ids():
            self.client_ips.append(id.get_ip())
        self.client_list.add_client_added_callback(lambda id: self.client_ips.append(id.get_ip()))

        self.thread = Thread(target=self._listen_for_new_clients, daemon=True)

    def start(self):
        self.thread.start()

    def _on_new_client(self, clientsocket, addr):
        client_name = None
        try:
            while True:
                data = clientsocket.recv(1024).decode()
                if data is not "":
                    # print(data)
                    json_data = json.loads(data)
                    return_data = []

                    if json_data[Constants.JSON_MESSAGE_TYPE] == Constants.JSON_MESSAGE_TYPE_POLL:
                        client_name = json_data[Constants.JSON_CLIENT_NAME]
                        user_id = json_data[Constants.JSON_USER_ID]

                        is_permitted = self.database.get_user_permission(user_id, client_name)

                        return_data[Constants.JSON_MESSAGE_TYPE] = Constants.JSON_MESSAGE_TYPE_DATA
                        return_data[Constants.JSON_CLIENT_NAME] = client_name
                        return_data[Constants.JSON_USER_ID] = user_id
                        return_data[Constants.JSON_USER_PERMISSION] = Constants.JSON_ACCESS_GRANTED if is_permitted else Constants.JSON_ACCESS_DENIED

                    elif json_data[Constants.JSON_MESSAGE_TYPE] == Constants.JSON_MESSAGE_TYPE_INSTALL_USER:
                        client_name = json_data[Constants.JSON_CLIENT_NAME]
                        user_id = json_data[Constants.JSON_USER_ID]
                        set_ok = self.database.add_user_permission(user_id, client_name)

                        return_data[Constants.JSON_MESSAGE_TYPE] = Constants.JSON_MESSAGE_TYPE_INSTALL_STATUS
                        return_data[Constants.JSON_STATUS] = Constants.JSON_STATUS_OK if set_ok else Constants.JSON_STATUS_FAIL

                    clientsocket.send(json.dumps(return_data).encode())

                sleep(1)
        except Exception as exptn:
            print("Exception:", exptn)
            if client_name is not None:
                self.client_list.remove_client(client_name, addr[0])
        finally:
            clientsocket.close()

    def _listen_for_new_clients(self):
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name

        s.bind((host, Constants.CLIENT_CONNECTION_PORT_NUMBER))
        s.listen(1)

        while True:
            c, addr = s.accept()  # Establish connection with client.
            if addr[0] in self.client_ips:
                new_thread = Thread(target=self._on_new_client, args=(c, addr), daemon=True)
                new_thread.start()
        s.close()