class User:

    def __init__(self, id):
        self.id = id
        self.permitted_clients = []
        self.admin = False

    def get_id(self):
        return self.id

    def get_permited_clients(self):
        return self.permitted_clients

    def is_admin(self):
        return self.admin

    def add_permitted_client(self, permitted_client_name):
        if permitted_client_name not in self.permitted_clients:
            self.permitted_clients.append(permitted_client_name)

    def set_admin(self, admin):
        self.admin = admin
