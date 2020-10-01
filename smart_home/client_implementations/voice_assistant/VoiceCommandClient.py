import json
import os
import re
import time
from threading import Thread, RLock

import speech_recognition as sr
from google.api_core.exceptions import ServiceUnavailable
from google.cloud import texttospeech as tts
from pygame import mixer

try:
    from snowboy.hotword_detection import HotwordDetector
except ImportError:
    pass

from smart_home.client.Client import Client
from smart_home.client_implementations.voice_assistant.commands.SwitchOnCommand import SwitchOnItemCommand
from smart_home.client_implementations.voice_assistant.commands.TimerCommand import TimerCommand
from smart_home.client_implementations.voice_assistant.commands.CancelCommand import CancelCommand
from smart_home.client_implementations.voice_assistant.sound_player import SoundPlayer


class VoiceCommandClient(Client):

    RESOURCES_FOLDER = "smart_home/resources/"
    MODEL_FILE = RESOURCES_FOLDER + "jarvis.umdl"
    CREDENTIALS_FILE = RESOURCES_FOLDER + "Jarvis-74f83c8acc1f.json"
    SOUNDS_FOLDER = RESOURCES_FOLDER + "sounds/"
    WAKE_TONE_FILE = SOUNDS_FOLDER + "WAKE_TONE.wav"
    SLEEP_TONE_FILE = SOUNDS_FOLDER + "SLEEP_TONE.wav"

    def __init__(self):
        super().__init__("JarvisVoiceCommand")
        self.recogniser = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recogniser_lock = RLock()
        with open(self.CREDENTIALS_FILE) as json_file:
            self.credentials_json = json_file.read()

        try:
            self.hotword_detector = HotwordDetector(self.MODEL_FILE)
        except NameError:
            print("Snowboy hotwork detectory not available")
            pass

        self.sound_player = SoundPlayer()

        self.commands = []

    def setup_process(self, server_connection):
        self.commands.append(SwitchOnItemCommand(self.sound_player, self.server_connection))
        self.commands.append(TimerCommand(self.sound_player, self.server_connection))
        self.commands.append(CancelCommand(self.sound_player, self.server_connection))

    def process(self, server_connection):
        # Snowboy await hotword
        # This blocks the main thread
        try:
            self.hotword_detector.start(self._listen)
            if self.hotword_detector.interrupted:
                exit()
        except AttributeError:
            # Snowboy not available
            # No hotword detector to start
            input("Hit enter to start listening\n")
            self._listen()

    def _listen(self):
        try:
            self.hotword_detector.stop()
        except AttributeError:
            # No hotword detector to stop
            pass
        try:
            self.recogniser_lock.acquire()
            with self.mic as source:
                self.recogniser.adjust_for_ambient_noise(source)

                # Listening tone
                # self._speak("I'm listening")
                self.sound_player.play(self.WAKE_TONE_FILE)
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
            self.sound_player.play(self.SLEEP_TONE_FILE)
            # print("Finished listening")
            pass

    def _process_command(self, parsed_speech):
        for command in self.commands:
            if command.consume(parsed_speech):
                return
        print(parsed_speech)
        self.sound_player.speak("I'm sorry, I don't know how to help with that")
        # print("I'm sorry, I don't know how to help with that")

    def _parse_speech(self, audio, callback):
        self.recogniser_lock.acquire()
        parsed_text = None
        try:
            parsed_text = self.recogniser.recognize_google_cloud(audio, language="en-GB", credentials_json=self.credentials_json)
        except sr.UnknownValueError:
            self.sound_player.speak("I'm sorry I didn't catch that")
            # print("I'm sorry I didn't catch that")
        except (sr.RequestError, ServiceUnavailable):
            self.sound_player.speak("I'm sorry, I seem to be having connection issues right now. Please try again")
            # print("I'm sorry, I seem to be having connection issues right now. Please try again")
        self.recogniser_lock.release()

        if parsed_text is not None:
            try:
                callback(parsed_text)
            except json.decoder.JSONDecodeError:
                self.sound_player.speak("I'm sorry, something went wrong. Please try again")


if __name__ == "__main__":
    client = VoiceCommandClient()
    client.start()
