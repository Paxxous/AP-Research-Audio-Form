from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot
)

import json
import pyaudio
import wave

CHUNK = 1024

with open("./res/instance1.json", "rb") as f:
    sessions = json.load(f)

class AudioHandler(QObject):
    finished = pyqtSignal()

    def __init__(self, filename=sessions["1"]["ref"]):
        super().__init__()

        self.filename = filename
        self._running = False
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.wav_file = None

    @pyqtSlot(str)
    def set_song(self, filename):
        if self._running:
            self.stop()
        self.filename = filename
        self.play_wav()

    @pyqtSlot()
    def play_wav(self):
        if self._running:
            return 

        self.wav_file = wave.open(self.filename, "rb")
        self._running = True

        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wav_file.getsampwidth()),
            channels=self.wav_file.getnchannels(),
            rate=self.wav_file.getframerate(),
            output=True,
            stream_callback=self._callback,
            frames_per_buffer=CHUNK
        )
        self.stream.start_stream()

    def _callback(self, in_data, frame_count, time_info, status):
        if not self._running:
            return (None, pyaudio.paComplete)

        data = self.wav_file.readframes(frame_count)

        if len(data) == 0:
            return (data, pyaudio.paComplete)

        return (data, pyaudio.paContinue)

    @pyqtSlot()
    def stop(self):
        if self._running:
            self._running = False

            # Close stream
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            # Close wav file
            if self.wav_file:
                self.wav_file.close()
                self.wav_file = None

            # Do NOT terminate self.p here
            self.finished.emit()


