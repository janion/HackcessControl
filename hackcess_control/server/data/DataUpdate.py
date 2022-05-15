import time
import hackcess_control.common.Constants as Constants


class DataUpdate:

    def __init__(self, value):
        self.value = value
        self.time = time.strftime(Constants.JSON_TIME_FORMAT)

    def get_value(self):
        return self.value

    def get_time(self):
        return self.time
