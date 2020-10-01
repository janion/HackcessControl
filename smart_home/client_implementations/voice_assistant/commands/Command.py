

class Command:

    def __init__(self, speak_callback, server_connection):
        self.speak_callback = speak_callback
        self.server_connection = server_connection

    def consume(self, command_text):
        raise NotImplementedError
