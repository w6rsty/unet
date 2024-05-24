from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import FlowLayout, ImageLabel
from typing import Callable

import os 
import config as cfg

class ImageSelectorPanel(QWidget):
    def __init__(self, imagePanel,parent=None):
        super().__init__(parent)
        self.imagePanel = imagePanel
        self.imageButtons = []
        for index, path in enumerate(cfg.DEMO_IMAGE_PATHS):
            bt = ImageButton(index, path)
            # bt.setCallback(lambda : info.set_data(index), reuslt.set_data(index))
            self.imageButtons.append(bt)

        self.addButton = ImageButton(-1, cfg.ADD_ICON_PATH)
        
        # 使用一个回调函数，这个回调函数在图片被点击时，要把图片展示到两个主页面，添加患者信息，添加分析报告
        for bt in self.imageButtons:
            bt.setCallback(lambda : self.imagePanel.set_image(index))
        
        self.initLayout()

    def initLayout(self):
        layout = FlowLayout(self, needAni = False)
        layout.setSpacing(20)

        for bt in self.imageButtons:
            layout.addWidget(bt)

        layout.addWidget(self.addButton)

        self.setLayout(layout)


class ImageButton(QToolButton):
    def __init__(self, id, imagePath, parent=None):
        super().__init__(parent)

        self.id = id

        self.setIcon(QIcon(os.path.abspath(imagePath)))
        self.setIconSize(QSize(200, 180))
        # self.initLayout()

    # def initLayout(self):
    #     layout = QVBoxLayout()
    #     layout.setAlignment(Qt.AlignCenter)

    #     layout.addWidget(self.imageLabel)

    #     self.setLayout(layout)

    def setCallback(self, callback: Callable[[int], None]):
        self.clicked.connect(lambda: callback(self.id))

    
