from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import (
    Qt,
    QObject,
    pyqtSignal
)

import json
import random

from enum import Enum
class Stg(Enum):
    CP = 1
    FP = 2

with open("./res/instance1.json", "r") as f:
    instance = json.load(f)

def shuffle_songs(inst):
    if inst == 1:
        hidden_sig = instance["1"]["hidden_signal"]
        fulldb_songs = list(instance["1"]["9db"].values()) + [hidden_sig]
        halfdb_songs = list(instance["1"]["4.5db"].values()) + [hidden_sig]


    elif inst == 2:
        hidden_sig = instance["2"]["hidden_signal"]
        fulldb_songs = list(instance["2"]["9db"].values()) + [hidden_sig]
        halfdb_songs = list(instance["2"]["4.5db"].values()) + [hidden_sig]

    else:
        raise ValueError("Invalid Instance")

    random.shuffle(fulldb_songs)
    random.shuffle(halfdb_songs)

    return fulldb_songs, halfdb_songs


class SessionHandler(QObject):
    session_state_changed = pyqtSignal(object, int, dict)

    def __init__(self):
        super().__init__()

        self.session = 1 # this remains constant until after our first tests

        self.trial = 1 # out of two
        self.stage = Stg.CP # CP or FP
        self.data = []

        self.finished = False

        self.trial_one_full_db_songs = {}
        self.trial_one_half_db_songs = {}

        self.trial_two_full_db_songs = {}
        self.trial_two_half_db_songs = {}

        l = ["A", "B", "C", "D", "E"]

        fulldb_songs, halfdb_songs = shuffle_songs(1)
        self.trial_one_full_db_songs = dict(zip(l, fulldb_songs))
        self.trial_one_half_db_songs = dict(zip(l, halfdb_songs))

        fulldb_songs, halfdb_songs = shuffle_songs(2)
        self.trial_two_full_db_songs = dict(zip(l, fulldb_songs))
        self.trial_two_half_db_songs = dict(zip(l, halfdb_songs))

        self.statusLabel = {}

        print(self.trial_one_full_db_songs)

    def make_sessions_status(self):
        session_status_layout = QVBoxLayout()
        session_status_layout.setSpacing(12)

        session_status = QLabel("t: 1, s: CP")
        session_status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.statusLabel = session_status

        session_status_layout.addWidget(session_status)

        return session_status_layout

    def get(self, f_path):
        for i, v in instance[str(self.trial)]["9db"].items():
            if v == f_path:
                return i

        for i, v in instance[str(self.trial)]["4.5db"].items():
            if v == f_path:
                return i
        
        if f_path == instance[str(self.trial)]["hidden_signal"]:
            return "hidden_signal"
        
        raise ValueError("directory not in file")
        # return "z - not real"
    
    def logit(self, items):
        if self.trial == 1 and self.stage == Stg.CP:
            song_dict = self.trial_one_full_db_songs
        elif self.trial == 1 and self.stage == Stg.FP:
            song_dict = self.trial_one_half_db_songs
        elif self.trial == 2 and self.stage == Stg.CP:
            song_dict = self.trial_two_full_db_songs
        elif self.trial == 2 and self.stage == Stg.FP:
            song_dict = self.trial_two_half_db_songs

        print(self.trial)
        # print(instance[str(self.trial)]["name"])
        lg = {
            "name": instance[str(self.trial)]["name"],
            "session": self.session,
            "trial": self.trial,
            "stage": self.stage.name,
            "ratings": {
                self.get(song_dict[eq_name]): v.value()
                for eq_name, v in items
                if v.isVisible()
            },
        }

        self.data.append(lg)
    

    def pick_song(self, key): # assign a song for each option that can be selected
        inst = instance[str(self.trial)]

        if key == "ref":
            return inst["ref"]

        elif self.trial == 1 and self.stage == Stg.CP:
            return self.trial_one_full_db_songs[key]

        elif self.trial == 1 and self.stage == Stg.FP:

            ratings = self.data[0]["ratings"]
            filtered_ratings = {k: v for k, v in ratings.items() if k != "hidden_signal"}
            maximum = max(filtered_ratings.items(), key=lambda item: item[1]) # the highest rated one

            if key == "A":
                # return "./res/audio/failsafe/candy.wav"
                return inst["9db"][maximum[0]]
            elif key == "B":
                # return "./res/audio/failsafe/candy.wav"
                return inst["4.5db"][maximum[0]]

        elif self.trial == 2 and self.stage == Stg.CP:
            return self.trial_two_full_db_songs[key]

        elif self.trial == 2 and self.stage == Stg.FP:
            ratings = self.data[2]["ratings"]
            filtered_ratings = {k: v for k, v in ratings.items() if k != "hidden_signal"}
            maximum = max(filtered_ratings.items(), key=lambda item: item[1]) # the highest rated one

            if key == "A":
                return inst["9db"][maximum[0]]
            elif key == "B":
                return inst["4.5db"][maximum[0]]

    def next_session(self):
        if self.trial == 1 and self.stage == Stg.CP: # move from the five eq options, the the two, with corresponding EQ
            self.stage = Stg.FP
            self.statusLabel.setText("t: 1, s: FP")

            self.session_state_changed.emit(self.stage, self.trial, self.trial_one_full_db_songs)

        elif self.trial == 1 and self.stage == Stg.FP: # go to the second session, give back the five EQ options
            self.stage = Stg.CP
            self.statusLabel.setText("t: 2, s: CP")

            self.session_state_changed.emit(self.stage, self.trial, self.trial_one_half_db_songs)

            self.trial += 1 # go forward after saving 

        elif self.trial == 2 and self.stage == Stg.CP: # once again, the two sliders and corresponding EQ
            self.stage = Stg.FP
            self.statusLabel.setText("t: 2, s: FP")

            self.session_state_changed.emit(self.stage, self.trial, self.trial_two_full_db_songs)

        elif self.trial == 2 and self.stage == Stg.FP: # dump the json into the data folder, and move on
            self.statusLabel.setText("FINISH")

            self.session_state_changed.emit(self.stage, self.trial, self.trial_two_half_db_songs)

            if self.finished == False:
                with open("./data/res.json", "w") as f:
                    json.dump(self.data, f, indent=4)

            self.finished = True
