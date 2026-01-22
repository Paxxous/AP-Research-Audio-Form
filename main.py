import sys

# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QGridLayout,
)

from functools import partial

from ui.scale import make_scale
from ui.sliders import make_slider_column
from ui.buttons import make_option_buttons, make_ref_button, make_next_button

from ui.input import inputHandler
from ui.session_handler import Stg, SessionHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("_")
        self.resize(800, 500)

        self.reference_buttons = {}
        self.sliders = {}
        self.progress_bar = {}

        self.dat = []

        self.inputHandler = inputHandler(self.reference_buttons, self.sliders)
        self.sessionHandler = SessionHandler()

        self.sessionHandler.session_state_changed.connect(self.on_session_state_changed)
        
        main_layout = QGridLayout();
        main_layout.addLayout(make_scale(), 1, 0)
        main_layout.setColumnStretch(1, 1)

        sliders_layout = QHBoxLayout()
        sliders_layout.setSpacing(25)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(25)

        for name in ["A", "B", "C", "D", "E"]:
            slider_layout, self.sliders[name] = make_slider_column(name)
            sliders_layout.addLayout(slider_layout)

            option_button_layout, self.reference_buttons[name] = make_option_buttons(name)
            buttons_layout.addLayout(option_button_layout)


        # add the sliders and the buttons below them
        main_layout.addLayout(sliders_layout, 1, 1)
        main_layout.addLayout(buttons_layout, 2, 1)

        # create the reference button
        ref_button_layout, ref_button = make_ref_button()

        for name, btn in self.reference_buttons.items():
            btn.clicked.connect(partial(self.inputHandler.on_button_pressed, self.sessionHandler, name))

        ref_button.clicked.connect(partial(self.inputHandler.ref_button_pressed, self.sessionHandler))
        main_layout.addLayout(ref_button_layout, 2, 0)

        # create the next button
        nxt_layout, self.next_button = make_next_button()
        self.next_button.clicked.connect(self.sessionHandler.next_session)

        main_layout.addLayout(nxt_layout, 0, 1)

        # create the session status
        main_layout.addLayout(self.sessionHandler.make_sessions_status(), 0, 0,)


        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


    def on_session_state_changed(self, stage, trial, session_songs): # we also write data here
        rem = ["C", "D", "E"] # these are the sliders that get removed and added a lot

        if stage == Stg.FP:
            self.sessionHandler.logit(self.sliders.items()) # the five options

            for i, v in self.sliders.items():
                if i in rem:
                    v.hide()
                    self.reference_buttons[i].hide()
                else:
                    v.setValue(0)

        elif stage == Stg.CP:
            self.sessionHandler.logit(self.sliders.items()) # the two options
            for i, v in self.sliders.items():
                v.setValue(0)
                v.show()

                self.reference_buttons[i].show()

    def closeEvent(self, e):
        self.inputHandler.delete()
        super().closeEvent(e)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())