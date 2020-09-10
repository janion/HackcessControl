from smart_home.server.connections.ClientId import ClientId


class ClientList:

    def __init__(self):
        self.client_ids = []
        self.client_added_callbacks = []

    def add_client(self, name, ip):
        existing_client = self._get_client_id(name, ip)
        if existing_client is None:
            newClient = ClientId(name, ip)
            self.client_ids.append(newClient)
            for callback in self.client_added_callbacks:
                callback(newClient)

    def get_client_ids(self):
        return self.client_ids.copy()

    def add_client_added_callback(self, callback):
        self.client_added_callbacks.append(callback)

    def _get_client_id(self, name="", ip=""):
        for client in self.client_ids:
            if client.get_ip() == ip or client.get_name() == name:
                return client
