from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import BodyLabel

class ResultInfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.titleBar = BodyLabel('Result Info')
        self.titleBar.setStyleSheet("\n"
"QLabel\n"
"{\n"
"    font: 15pt \"Microsoft YaHei UI\";\n"
"border-radius: 50px;\n"
"border: 2px solid grey;\n"
"background-color: rgb(62, 144, 162);\n"
"\n"
"}")
        self.titleBar.setFixedWidth(200)  # 设置标题栏的宽度为200像素
        self.titleBar.setFixedHeight(50)   # 设置标题栏的高度为50像素


        self.infoText = BodyLabel('This is the patient result info panel')
        self.infoText.setStyleSheet("QLabel {border: 2px solid grey;}")
        self.infoText.setFixedWidth(200)  # 设置信息文本的宽度为200像素
        self.infoText.setFixedHeight(30)   # 设置信息文本的高度为30像素
        
        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.titleBar)
        layout.addWidget(self.infoText)

        self.setLayout(layout)
        
        
    # def set_data(self, data):
      