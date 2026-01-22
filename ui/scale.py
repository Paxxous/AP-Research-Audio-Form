from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
)

def make_scale():
    scale = QVBoxLayout()
    scale.setSpacing(12)

    labels = [
        "Much better",
        "Better",
        "Slightly better",
        "The same",
        "Slightly worse",
        "Worse",
        "Much worse",
    ]

    for text in labels:
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        scale.addWidget(lbl, stretch=1)

    # reference = QPushButton("REF")
    # scale.addWidget(reference)

    scale.addStretch()
    return scale