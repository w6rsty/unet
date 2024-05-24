from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import FlowLayout, ImageLabel
from typing import Callable

import config as cfg


class ImageSelectorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.imageButtons = []
        for index, path in enumerate(cfg.DEMO_IMAGE_PATHS):
            bt = ImageButton(index, path)
            self.imageButtons.append(bt)
        
        self.addButton = ImageButton(-1, cfg.ADD_ICON_PATH)

        self.initLayout()

    def initLayout(self):
        layout = FlowLayout(self, needAni = False)
        layout.setSpacing(20)

        for bt in self.imageButtons:
            layout.addWidget(bt)

        layout.addWidget(self.addButton)

        self.setLayout(layout)


class ImageButton(QWidget):
    def __init__(self, id, imagePath, parent=None):
        super().__init__(parent)

        self.id = id

        self.imageLabel = ImageLabel(imagePath)
        self.imageLabel.setFixedSize(200, 180)
        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.imageLabel)

        self.setLayout(layout)