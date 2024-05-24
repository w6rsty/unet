from PyQt5.QtWidgets import QWidget, QToolButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import config as cfg

class Toolbar(QWidget):
    def __init__(self, model, painter, parent=None):
        super().__init__(parent)

        self.model = model
        self.painter = painter

        self.bts = []
        
        for index, info in enumerate(cfg.TOOL_BUTTON_INFOS):
            bt = IconTextButton(info[0], info[1])
            self.bts.append(bt)

        self.bts[0].setCallBack(self.painter.load_image)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        for bt in self.bts:
            bt.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            layout.addWidget(bt)

        self.setLayout(layout)

        
class IconTextButton(QToolButton):
    def __init__(self, title, path, parent=None):
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
    
    def setCallBack(self, callback):
        self.clicked.connect(callback)