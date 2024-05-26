from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt


class ResultInfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        self.setLayout(layout)