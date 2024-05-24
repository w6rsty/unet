from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from qfluentwidgets import ImageLabel

import config as cfg

class ImageManipulatePanel(QWidget):
    def __init__(self,jsonLibrary,parent=None):
        super().__init__(parent)
        self.jsonlibrary = jsonLibrary
        self.manipulatedImage = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)
        self.originalImage = ImageLabel(cfg.PLACEHOLDER_IMAGE_PATH)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.manipulatedImage)
        layout.addWidget(self.originalImage)
        self.setLayout(layout)
        
    def set_image(self, id):
        json = self.jsonlibrary.getJsonById(id+1)
        self.manipulatedImage.setPixmap(QPixmap(json["imgPath"]))
        self.originalImage.setPixmap(QPixmap(json["imgPath"]))