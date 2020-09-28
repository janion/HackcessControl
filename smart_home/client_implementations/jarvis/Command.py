

class CommandRegex:

    def __init__(self, regex, the_group, item_group, action_group, value_group):
        self.regex = regex
        self.the_group = the_group
        self.item_group = item_group
        self.action_group = action_group
        self.value_group = value_group


class Command:

    def __init__(self, speak_callback, server_connection):
        self.speak_callback = speak_callback
        self.server_connection = server_connection

    def consume(self, command_text):
        raise NotImplementedError
