from smart_home.client_implementations.voice_assistant.commands.Command import Command


class CancelCommand(Command):

    CANCEL = "cancel"

    def consume(self, parsed_speech):
        if self.CANCEL in parsed_speech:
            self.sound_player.speak("Never mind")
            return True
        return False
