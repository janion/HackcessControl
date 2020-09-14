from smart_home.server.data.DataUpdate import DataUpdate
from smart_home.server.data.DataField import DataField
import smart_home.common.Constants as Constants


class Database:

    def __init__(self):
        self.data = {}

    def add_field(self, field_name, permitted_ip=Constants.ANY_IP, initial_value=0):
        if self._get_field(field_name) is not None:
            return False

        field = DataField(field_name, permitted_ip)
        self.data[field] = DataUpdate(initial_value)

        return True

    def set_field_value(self, field_name, value, ip):
        field = self._get_field(field_name)
        if field is None or not field.has_permission(ip):
            return False

        self.data[field] = DataUpdate(value)
        return True

    def get_field_value(self, field_name):
        return self.data[self._get_field(field_name)]

    def _get_field(self, name):
        for field in self.data.keys():
            if field.get_name() == name:
                return field
