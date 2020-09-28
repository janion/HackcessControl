from smart_home.client_implementations.jarvis.Command import Command


class CancelCommand(Command):

    CANCEL = "cancel"

    def consume(self, parsed_speech):
        if self.CANCEL in parsed_speech:
            self.speak_callback("Never mind")
            return True
        return False
