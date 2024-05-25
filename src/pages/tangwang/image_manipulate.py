from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from qfluentwidgets import ImageLabel

import config as cfg

class ImageManipulatePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.manipulatedImage = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)
        self.originalImage = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.manipulatedImage)
        layout.addWidget(self.originalImage)
        self.setLayout(layout)
        
