from threading import RLock

from hackcess_control.server.data.User import User


class Database:

    def __init__(self):
        self.users = {}
        self.lock = RLock()

    def add_user_permission(self, user_id, permitted_client_name):
        self.lock.acquire()

        user = self.users[user_id]
        if user is None:
            user = User(user_id)
            self.users[user_id] = user

        user.add_permitted_client(permitted_client_name)

        self.lock.release()
        return True

    def get_user_permission(self, user_id, client_name):
        self.lock.acquire()

        user = self.users[user_id]
        if user is not None:
            self.lock.release()
            return client_name in user.get_permited_clients()
        else:
            self.lock.release()
            return False

    def get_user_admin_status(self, user_id):
        self.lock.acquire()

        user = self.users[user_id]
        if user is not None:
            self.lock.release()
            return user.is_admin()
        else:
            self.lock.release()
            return False
