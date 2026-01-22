from PyQt6.QtCore import (
    QObject,
    QThread,
    pyqtSignal
)

from ui.audio_handler import AudioHandler

import json

with open("./res/instance1.json", "r") as f:
    sessions = json.load(f)

SESSION = ""

class inputHandler(QObject):
    play_requested = pyqtSignal(str)
    stop_requested = pyqtSignal()

    def __init__(self, reference_buttons, sliders):
        super().__init__()
        self.reference_buttons = reference_buttons
        self.sliders = sliders

        self.is_playing = False

        # Worker thread + AudioHandler
        self.audio_thread = QThread(self)
        self.audio_handler = AudioHandler()
        self.audio_handler.moveToThread(self.audio_thread)

        self.play_requested.connect(self.audio_handler.set_song)
        self.stop_requested.connect(self.audio_handler.stop)
        self.audio_handler.finished.connect(self._on_audio_finished)

        self.audio_thread.finished.connect(self.audio_handler.deleteLater)
        self.audio_thread.finished.connect(self.audio_thread.deleteLater)
        self.audio_thread.start()

    def delete(self):
        self.stop_requested.emit()
        self.audio_thread.quit()
        self.audio_thread.wait()

    def on_button_pressed(self, shndlr, name):
        btn = self.sender()
        key = name

        if self.is_playing:
            self.stop_requested.emit()
        else:
            self.play_requested.emit(shndlr.pick_song(key))
            self.is_playing = True

    def _on_audio_finished(self):
        self.is_playing = False

    def ref_button_pressed(self, shndlr):
        if self.is_playing:
            self.stop_requested.emit()
        else:
            self.play_requested.emit(shndlr.pick_song("ref"))
            self.is_playing = True
