from PyQt5.QtWidgets import QWidget, QToolButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import config as cfg

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        for button in cfg.TOOL_BUTTON_INFOS:
            button = IconTextButton(button[0], button[1])
            button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
            layout.addWidget(button)

        self.setLayout(layout)

#IconTextButton类是QToolButton的子类，它通过设置按钮的标题、字体、图标以及样式来创建一个带有图标和文本的按钮。
# 在IconTextButton类中还重写了heightForWidth方法，以保持按钮的宽高比为1:1。        
class IconTextButton(QToolButton):
    def __init__(self, title, path,parent=None):
        super().__init__(parent)
        self.setObjectName(title)
        
        self.setText(title)
        self.setFont(QFont(cfg.TOOL_BUTTON_FONT_NAME, cfg.TOOL_BUTTON_FONT_SIZE))

        icon = QIcon(path)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)

    # Overwrite the heightForWidth method to keep aspect ratio 1:1
    def heightForWidth(self, width):
        return width