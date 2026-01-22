from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QSlider,
    QPushButton,
    QVBoxLayout,
    QSizePolicy,
)

def make_slider_column(name: str):
    col = QVBoxLayout()
    col.setSpacing(5)

    # up_btn = QPushButton("▲")
    # down_btn = QPushButton("▼")

    # up_btn.setFixedHeight(20)
    # down_btn.setFixedHeight(20)

    slider = QSlider(Qt.Orientation.Vertical)
    slider.setRange(-100, 100)
    slider.setValue(0)

    slider.setTickPosition(QSlider.TickPosition.NoTicks)
    slider.setSizePolicy(
        QSizePolicy.Policy.Preferred,
        QSizePolicy.Policy.Expanding
    )

    # button behavior
    # up_btn.clicked.connect(lambda: slider.setValue(slider.value() + 1))
    # down_btn.clicked.connect(lambda: slider.setValue(slider.value() - 1))

    # col.addWidget(up_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    col.addWidget(slider, stretch=1)
    # col.addWidget(down_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    return col, slider
