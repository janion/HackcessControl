import time
import os
import re
from threading import RLock

from google.cloud import texttospeech as tts
from google.oauth2 import service_account
from pygame import mixer


class SoundPlayer:

    RESOURCES_FOLDER = "smart_home/resources/"
    CREDENTIALS_FILE = RESOURCES_FOLDER + "Jarvis-74f83c8acc1f.json"
    SOUNDS_FOLDER = RESOURCES_FOLDER + "sounds/"

    def __init__(self):
        self.speaker_lock = RLock()

        self.voice_params = tts.VoiceSelectionParams(language_code="en-GB", name="en-GB-Wavenet-B")
        self.audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        self.client = tts.TextToSpeechClient(credentials=service_account.Credentials.from_service_account_file(self.CREDENTIALS_FILE))

        mixer.init()
        self.speech_filenames = {}

    # def speak(self, text):
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

    def speak(self, *text):
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
        self.play(*files_to_speak)

    def _convert_text_to_filename(self, text):
        if text in self.speech_filenames.keys():
            return self.speech_filenames[text]
        else:
            filename = self.SOUNDS_FOLDER + re.subn("([^a-zA-Z0-9 ]+)", "", text)[0].replace(" ", "_").lower() + ".wav"
            self.speech_filenames[text] = filename
            return filename

    def play(self, *files_to_play):
        self.speaker_lock.acquire()
        for file_to_play in files_to_play:
            mixer.music.load(file_to_play)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
        self.speaker_lock.release()
