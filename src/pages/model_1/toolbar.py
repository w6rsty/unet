from PyQt5.QtWidgets import QWidget, QToolButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

import config as cfg

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons = [
            IconTextButton('加载图片', 'assets/icons/加载图片.png'),
            IconTextButton('读取历史', 'assets/icons/读取历史.png'),
            IconTextButton('大图识别', 'assets/icons/大图识别.png'),
            IconTextButton('矩形增加', 'assets/icons/矩形增加.png'),
            IconTextButton('手动添加', 'assets/icons/手动添加.png'),
            IconTextButton('矩形删除', 'assets/icons/矩形删除.png'),
            IconTextButton('手动删除', 'assets/icons/手动删除.png'),
            IconTextButton('区域生长', 'assets/icons/区域生长.png'),
            IconTextButton('眼底分区', 'assets/icons/眼底分区.png'),
            IconTextButton('矩形分区', 'assets/icons/矩形分区.png'),
            IconTextButton('撤销操作', 'assets/icons/撤销操作.png'),
            IconTextButton('数据保存', 'assets/icons/数据保存.png'),
            IconTextButton('掩膜保存', 'assets/icons/掩模保存.png'),
        ]

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        for button in self.buttons:
            layout.addWidget(button)

        self.setLayout(layout)

        
class IconTextButton(QToolButton):
    def __init__(self, title, path, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        
        self.setText(title)
        self.setFont(

        icon = QIcon(path)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon | Qt.AlignCenter)
        self.setAutoRaise(True)

    # Overwrite the heightForWidth method to keep aspect ratio 1:1
    def heightForWidth(self, width):
        return width