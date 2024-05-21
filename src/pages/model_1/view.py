from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from .toolbar import Toolbar

class Model1View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Model1View')

        self.toolbar = Toolbar(self)

        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)