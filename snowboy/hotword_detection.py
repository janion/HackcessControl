import signal
from snowboy import snowboydecoder


class HotwordDetector:

    def __init__(self, model):
        self.interrupted = False
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        self.detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

    def start(self, callback):
        self.detector.start(detected_callback=callback, interrupt_check=self.interrupt_callback, sleep_time=0.03)
        self.stop()

    def stop(self):
        self.detector.terminate()

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted
