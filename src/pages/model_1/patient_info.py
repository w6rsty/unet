from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import BodyLabel

class PatientInfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleBar = BodyLabel('Patient Info')
        self.titleBar.setStyleSheet("\n"
"QLabel\n"
"{\n"
"    font: 15pt \"Microsoft YaHei UI\";\n"
"border-radius: 50px;\n"
"border: 2px solid grey;\n"
"background-color: rgb(62, 144, 162);\n"
"\n"
"}")
        self.infoText = BodyLabel('This is the patient info panel')

        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.titleBar)
        layout.addWidget(self.infoText)

        self.setLayout(layout)

    # def set_data(self, index):
    #     self.setText(f'Patient Info {index}')