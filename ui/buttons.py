# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)

def make_option_buttons(name):
    option = QHBoxLayout()
    option.setSpacing(25)

    # opt_buttons = {}


    # for name in ["A", "B", "C", "D", "E"]:
    btn = QPushButton(name)

    btn.setSizePolicy(
        QSizePolicy.Policy.Minimum,
        QSizePolicy.Policy.Fixed
    )

    option.addWidget(btn)

    return option, btn

def make_ref_button():
    ref = QHBoxLayout()
    ref.setSpacing(25)

    ref_btn = QPushButton("REF")

    ref_btn.setSizePolicy(
        QSizePolicy.Policy.Minimum,
        QSizePolicy.Policy.Fixed
    )

    ref.addWidget(ref_btn)

    return ref, ref_btn

def make_next_button():
    nxt_layout = QHBoxLayout()
    nxt_layout.setSpacing(25)

    nxt_button = QPushButton("NEXT")

    nxt_button.setSizePolicy(
        QSizePolicy.Policy.Minimum,
        QSizePolicy.Policy.Fixed
    )

    nxt_layout.addWidget(nxt_button)

    return nxt_layout, nxt_button
