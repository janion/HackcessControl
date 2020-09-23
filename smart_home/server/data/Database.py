from threading import RLock

from smart_home.server.data.DataUpdate import DataUpdate
from smart_home.server.data.DataField import DataField
import smart_home.common.Constants as Constants


class Database:

    def __init__(self):
        self.data = {}
        self.lock = RLock()

    def add_field(self, field_name, permitted_ip=Constants.ANY_IP, initial_value=0):
        self.lock.acquire()

        if self._get_field(field_name) is not None:
            self.lock.release()
            return False

        field = DataField(field_name, permitted_ip)
        self.data[field] = DataUpdate(initial_value)

        self.lock.release()
        return True

    def set_field_value(self, field_name, value, ip):
        self.lock.acquire()

        field = self._get_field(field_name)
        if field is None or not field.has_permission(ip):
            self.lock.release()
            return False

        self.data[field] = DataUpdate(value)

        self.lock.release()
        return True

    def get_field_value(self, field_name):
        self.lock.acquire()

        field = self._get_field(field_name)
        if field is not None:
            self.lock.release()
            return self.data[field]
        else:
            self.lock.release()
            return None

    def get_field_names(self):
        return [key.get_name() for key in self.data.keys()]

    def _get_field(self, name):
        for field in self.data.keys():
            if field.get_name() == name:
                return field
        return None
