from PyQt5.QtWidgets import QWidget

class Model2View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('Model2View')
        self.setStyleSheet('background-color: blue;')