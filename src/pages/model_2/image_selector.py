from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from qfluentwidgets import FlowLayout, ImageLabel

import config as cfg


class ImageSelectorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.imageButtons = [ImageButton(cfg.PLACEHOLDER_IMAGE_PATH) for _ in range(5)]
        
        self.addButton = ImageButton(cfg.ADD_ICON_PATH)

        self.initLayout()

    def initLayout(self):
        layout = FlowLayout(self, needAni = False)
        layout.setSpacing(20)

        for imageButton in self.imageButtons:
            layout.addWidget(imageButton)

        layout.addWidget(self.addButton)

        self.setLayout(layout)


class ImageButton(QWidget):
    def __init__(self, imagePath, parent=None):
        super().__init__(parent)

        self.imageLabel = ImageLabel(imagePath)
        self.imageLabel.setFixedSize(200, 180)
        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.imageLabel)

        self.setLayout(layout)
        

        