import time
import re
import os
import json
import speech_recognition as sr
from threading import Thread, RLock
from google.cloud import texttospeech as tts
from google.oauth2 import service_account
from google.api_core.exceptions import ServiceUnavailable
from pygame import mixer

from smart_home.client.Client import Client
import smart_home.common.Constants as Constants


class VoiceCommandClient(Client):

    class Command:

        def __init__(self, regex, item_group, action_group):
            self.regex = regex
            self.item_group = item_group
            self.action_group = action_group

    BACKGROUND_ADJUSTMENT_PERIOD = 20

    # Almost worked: "(?:please ?)?turn (on|off) (?:the ?)?(.*)(?: please?)?"
    COMMANDS = [Command(".*?[turn|switch] (%s|%s) (?:the ?)?(.*)" % (Constants.ON, Constants.OFF), 2, 1),
                Command(".*?[turn|switch] (?:the ?)?(.*) (%s|%s)" % (Constants.ON, Constants.OFF), 1, 2)
                ]

    CREDENTIALS_FILE = "Jarvis-74f83c8acc1f.json"
    WAKE_TONE_FILE = "wake.wav"
    SLEEP_TONE_FILE = "sleep.wav"

    def __init__(self):
        super().__init__("JarvisVoiceCommand")
        self.recogniser = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recogniser_lock = RLock()
        self.speaker_lock = RLock()
        with open(self.CREDENTIALS_FILE) as json_file:
            self.credentials_json = json_file.read()

        self.voice_params = tts.VoiceSelectionParams(language_code="en-GB", name="en-GB-Wavenet-B")
        self.audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        self.client = tts.TextToSpeechClient(credentials=service_account.Credentials.from_service_account_file(self.CREDENTIALS_FILE))

        mixer.init()
        self.speech_filenames = {}

    def setup_process(self, server_connection):
        # Start snowboy
        pass

    def process(self, server_connection):
        # Snowboy await hotword
        self._listen()

    def _listen(self):
        try:
            self.recogniser_lock.acquire()
            with self.mic as source:
                self.recogniser.adjust_for_ambient_noise(source)

                # Listening tone
                # self._speak("I'm listening")
                self._play(self.WAKE_TONE_FILE)
                # print("Listening")

                audio = self.recogniser.listen(source, timeout=5, phrase_time_limit=10)
                processing_thread = Thread(target=self._parse_speech, args=(audio, self._process_command))
                processing_thread.start()
            self.recogniser_lock.release()
        except sr.WaitTimeoutError:
            # print("Wait timeout")
            pass
        finally:
            # End listening tone
            # self._speak("Finished listening")
            self._play(self.SLEEP_TONE_FILE)
            # print("Finished listening")
            pass

    def _process_command(self, parsed_speech):
        for command in self.COMMANDS:
            match = re.match(command.regex, parsed_speech.replace(" please", "").replace("please ", ""))
            if match:
                item = match.group(command.item_group).strip()
                action = match.group(command.action_group)
                return_data = self.server_connection.update_field(item, action)
                if return_data[Constants.JSON_STATUS] == Constants.JSON_STATUS_OK:
                    self._speak("OK")
                    # print("OK")
                elif return_data[Constants.JSON_STATUS] == Constants.JSON_STATUS_FAIL:
                    self._speak("I'm sorry, I don't know about", item.replace("my", "your"))
                    # print("I'm sorry, I don't know about %s" % item.replace("my", "your"))
                return
        self._speak("I'm sorry, I don't know how to help with that")
        # print("I'm sorry, I don't know how to help with that")

    def _parse_speech(self, audio, callback):
        self.recogniser_lock.acquire()
        parsed_text = None
        try:
            parsed_text = self.recogniser.recognize_google_cloud(audio, language="en-GB", credentials_json=self.credentials_json)
        except sr.UnknownValueError:
            self._speak("I'm sorry I didn't catch that")
            # print("I'm sorry I didn't catch that")
        except (sr.RequestError, ServiceUnavailable):
            self._speak("I'm sorry, I seem to be having connection issues right now. Please try again")
            # print("I'm sorry, I seem to be having connection issues right now. Please try again")
        self.recogniser_lock.release()

        if parsed_text is not None:
            try:
                callback(parsed_text)
            except json.decoder.JSONDecodeError:
                self._speak("I'm sorry, something went wrong. Please try again")

    # def _speak(self, text):
    #     text_input = tts.SynthesisInput(text=text)
    #     response = self.client.synthesize_speech(input=text_input, voice=self.voice_params, audio_config=self.audio_config)
    #
    #     filename = self._convert_text_to_filename(text)
    #     if not os.path.exists(filename):
    #         with open(filename, 'wb') as out:
    #             out.write(response.audio_content)
    #             print(f'Audio content written to "{filename}"')
    #
    #     self.speaker_lock.acquire()
    #     mixer.music.load(filename)
    #     mixer.music.play()
    #     while mixer.music.get_busy():
    #         time.sleep(0.2)
    #     self.speaker_lock.release()

    def _speak(self, *text):
        files_to_speak = []
        for each_text in text:
            text_input = tts.SynthesisInput(text=each_text)
            response = self.client.synthesize_speech(input=text_input, voice=self.voice_params, audio_config=self.audio_config)

            filename = self._convert_text_to_filename(each_text)
            if not os.path.exists(filename):
                with open(filename, 'wb') as out:
                    out.write(response.audio_content)
                    print(f'Audio content written to "{filename}"')
            files_to_speak.append(filename)
        self._play(*files_to_speak)

    def _convert_text_to_filename(self, text):
        if text in self.speech_filenames.keys():
            return self.speech_filenames[text]
        else:
            filename = re.subn("([^a-zA-Z ]+)", "", text)[0].replace(" ", "_").lower() + ".wav"
            self.speech_filenames[text] = filename
            return filename

    def _play(self, *files_to_play):
        self.speaker_lock.acquire()
        for file_to_play in files_to_play:
            mixer.music.load(file_to_play)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
        self.speaker_lock.release()


if __name__ == "__main__":
    client = VoiceCommandClient()
    client.start()
