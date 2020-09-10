import socket
import json
from threading import Thread

import smart_home.common.Constants as Constants


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
        try:
            while True:
                data = clientsocket.recv(1024).decode()
                # print(data)
                json_data = json.loads(data)
                if json_data[Constants.JSON_MESSAGE_TYPE] == Constants.JSON_MESSAGE_TYPE_POLL:
                    data_type = json_data[Constants.JSON_DATA_TYPE]
                    value = self.database.get_field_value(data_type).get_value()
                    return_data = {data_type: value}
                    clientsocket.send(json.dumps(return_data).encode())
        except:
            pass
            self.client_list.remove_client(addr[0])
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