import time


class DataUpdate:

    def __init__(self, value):
        self.value = value
        self.time = time.localtime()

    def get_value(self):
        return self.value

    def get_time(self):
        return self.time
