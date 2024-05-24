from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import FlowLayout, ImageLabel
from typing import Callable

import os 
import config as cfg

class ImageSelectorPanel(QWidget):
    def __init__(self, patient_info, result_info, parent=None):
        super().__init__(parent)
    
        self.imageButtons = []
        for index, path in enumerate(cfg.DEMO_IMAGE_PATHS):
            bt = ImageButton(index, path, patient_info, result_info)
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


class ImageButton(QToolButton):
    def __init__(self, id, imagePath, patient_info = None, result_info = None, parent=None):
        super().__init__(parent)

        self.id = id

        self.setIcon(QIcon(os.path.abspath(imagePath)))
        self.setIconSize(QSize(200, 180))
        self.initLayout()

        self.patient_info = patient_info
        self.result_info = result_info
        self.clicked.connect(lambda: self.notify(id))

    def initLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def notify(self, id):
        self.patient_info.set_data(id)
        self.result_info.set_data(id)

    
