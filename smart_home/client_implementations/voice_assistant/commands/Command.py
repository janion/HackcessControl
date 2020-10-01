

class Command:

    def __init__(self, sound_player, server_connection):
        self.sound_player = sound_player
        self.server_connection = server_connection

    def consume(self, command_text):
        raise NotImplementedError
