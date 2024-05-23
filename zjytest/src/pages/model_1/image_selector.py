from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from qfluentwidgets import FlowLayout, ImageLabel
from PyQt5.QtGui import QImage, QPixmap

import config as cfg
import sys,os
pypath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src/function')
sys.path.append(pypath)
import function as fuc 

class ImageSelectorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.imageButtons = [ImageButton(cfg.PLACEHOLDER_IMAGE_PATH) for _ in range(5)]
        
        for i, button in enumerate(self.imageButtons):
            button.setImage(i+1)
        
        self.addButton = ImageButton(cfg.ADD_ICON_PATH)

        self.initLayout()

    def initLayout(self):
        layout = FlowLayout(self, needAni = False)
        layout.setSpacing(20)

        for imageButton in self.imageButtons:
            layout.addWidget(imageButton)


        
        layout.addWidget(self.addButton)

        self.setLayout(layout)


class ImageButton(QWidget):
    def __init__(self, imagePath, parent=None):
        super().__init__(parent)

        self.imageLabel = ImageLabel(imagePath)
        self.imageLabel.setFixedSize(200, 180)
        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.imageLabel)

        self.setLayout(layout)
    
    def setImage(self, i):
        jsonData = fuc.getJson(i)
        img_path = jsonData['imgPath']
         # 加载图片
        image = QImage(img_path)
        if image.isNull():
            print("Failed to load image:", img_path)
            return

        # 缩放图片到200x180，保持宽高比
        scaled_image = image.scaled(200, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 转换为QPixmap并设置给imageLabel
        pixmap = QPixmap.fromImage(scaled_image)
        self.imageLabel.setPixmap(pixmap)