from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from qfluentwidgets import ImageLabel

import config as cfg

class ImageManipulatePanel(QWidget):
    def __init__(self,jsonLibrary,parent=None):
        super().__init__(parent)
        self.jsonlibrary = jsonLibrary

        self.splitter = QSplitter(Qt.Horizontal)

        self.imageLeft = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)
        self.imageRight = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.splitter)
        
        self.splitter.addWidget(self.imageLeft)
        self.splitter.addWidget(self.imageRight)
        
        self.setLayout(layout)

        
    def setImageLeft(self, path):
        self.imageLeft.setImage(path)