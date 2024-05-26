from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import BodyLabel

class PatientInfoPanel(QWidget):
    def __init__(self, jsonLibrary, parent=None):
        super().__init__(parent)

        self.jsonlibrary = jsonLibrary

        self.titleBar = BodyLabel('病人信息')
        self.titleBar.setFixedHeight(50)
        self.titleBar.setAlignment(Qt.AlignCenter)        
        self.titleBar.setStyleSheet(
            "QLabel\n"
            "{\n"
            "font: 15pt \"Microsoft YaHei UI\";\n"
            "border-radius: 50px;\n"
            "border: 2px solid grey;\n"
            "background-color: rgb(62, 144, 162);\n"
            "}"
        )

        self.infoText = BodyLabel('')
        
        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.titleBar)
        layout.addWidget(self.infoText, 0, Qt.AlignTop | Qt.AlignLeft)

        self.setLayout(layout)

    def set_data(self, index):
        text = ""
        for key, value in self.jsonlibrary.getJsonById(index)['patientInfo'].items():
            text += key + ": " + value + "\n"
        self.infoText.setText(text)