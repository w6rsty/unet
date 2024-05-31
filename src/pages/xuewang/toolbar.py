from PyQt5.QtWidgets import QWidget, QToolButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

import src.config as cfg

class Toolbar(QWidget):
    def __init__(self, model, dispatch, parent=None):
        super().__init__(parent)

        # 模型的引用
        self.model = model

        self.bts = []
        for info in cfg.XUEWANG_TOOL_BUTTON_INFOS:
            bt = IconTextButton(info[0], info[1])
            self.bts.append(bt)

        # 设置按钮的回调函数
        self.bts[0].setCallBack(dispatch.imagePanel.loadImage)
        self.bts[1].setCallBack(dispatch.imagePanel.readHistory)
        self.bts[2].setCallBack(dispatch.imagePanel.globalRecognize)
        # self.bts[3].setCallBack(dispatch.imagePanel.addRect)
        # self.bts[4].setCallBack(dispatch.imagePanel.deleteRect)
        # self.bts[5].setCallBack(dispatch.imagePanel.manualAdd)
        # self.bts[6].setCallBack(dispatch.imagePanel.manualDelete)
        # self.bts[7].setCallBack(dispatch.imagePanel.regionGrow)
        # self.bts[3].setCallBack(dispatch.imagePanel.undo)
        self.bts[3].setCallBack(dispatch.imagePanel.saveData)
        # self.bts[4].setCallBack(dispatch.imagePanel.saveMask)

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
        self.setIconSize(QSize(40, 40))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)

    # # Overwrite the heightForWidth method to keep aspect ratio 1:1
    # def heightForWidth(self, width):
    #     return width
    
    def setCallBack(self, callback):
        self.clicked.connect(callback)
