from hackcess_control.server.connections.ClientId import ClientId


class ClientList:

    def __init__(self):
        self.client_ids = []
        self.client_added_callbacks = []

    def add_client(self, name, ip):
        existing_client = self._get_client_id(name, ip)
        if existing_client is not None:
            return True

        existing_named_client = self._get_client_id(name)
        if existing_named_client is None:
            new_client = ClientId(name, ip)
            self.client_ids.append(new_client)
            for callback in self.client_added_callbacks:
                callback(new_client)
            return True
        return False

    def remove_client(self, name, ip):
        existing_client = self._get_client_id(name, ip)
        if existing_client is not None:
            self.client_ids.remove(existing_client)
            return True
        return False

    def get_client_ids(self):
        return self.client_ids.copy()

    def add_client_added_callback(self, callback):
        self.client_added_callbacks.append(callback)

    def _get_client_id(self, name=None, ip=None):
        for client in self.client_ids:
            if name is not None and ip is not None and client.get_name() == name and client.get_ip() == ip:
                return client
            elif name is not None and ip is None and client.get_name() == name:
                return client
            elif ip is not None and name is None and client.get_ip() == ip:
                return client
        return None
