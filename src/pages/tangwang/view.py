from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class Model2View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Model2View')
    
        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget

        self.setLayout(layout)