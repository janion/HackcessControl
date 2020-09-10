import smart_home.common.Constants as Constants


class DataField:

    def __init__(self, name, permitted_ip=Constants.ANY_IP):
        self.name = name
        self.permitted_ip = permitted_ip

    def get_name(self):
        return self.name

    def has_permission(self, ip):
        if self.permitted_ip is Constants.ANY_IP:
            return True
        else:
            return ip == self.permitted_ip
