from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QGraphicsView, QGraphicsScene, QSizePolicy, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QImage, QColor, QPen, QBrush, QPainter
from PyQt5.QtCore import Qt
from skimage import io
import numpy as np
from PIL import Image
from enum import Enum

import config as cfg

class OperationMode(Enum):
    NONE = -1           # 无操作
    GLOBAL_RECOGNIZE = 0    # 大图识别
    ADD_RECT = 1        # 矩形增加
    DELETE_RECT = 2     # 矩形删除
    MANUAL_ADD = 3     # 手动添加
    MANUAL_DELETE = 4   # 手动删除
    REGION_GROW = 5     # 区域生长
    RETINA_SEG = 6      # 眼底分区
    RECT_RATIO = 7      # 矩形占比

def np2pixmap(np_img):
    height, width, _ = np_img.shape
    bytesPerLine = 3 * width
    qImg = QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

class ImageManipulatePanel(QWidget):
    def __init__(self, jsonLibrary, mode, parent=None):
        super().__init__(parent)

        self.jsonlibrary = jsonLibrary

        # 功能模式
        self.mode = mode
        # 图像大小
        self.imageSize = None
        # 原始图像数据
        self.imageData = None # NDArray
        # 会被修改的图像数据
        self.manipulatedData = None

        self.start_pos = None
        self.end_pos = None

        self.is_mouse_down = False


        self.pen = QPen(QColor(255, 0, 0))
        self.pen.setWidth(2)
        #################################################################
        # 分隔
        self.splitter = QSplitter(Qt.Horizontal)

        self.imageViewLeft = QGraphicsView()
        self.imageSceneLeft = None
        self.imageViewLeft.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageViewLeft.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageViewLeft.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.imageViewRight = QGraphicsView()
        self.imageSceneRight = None
        self.imageViewRight.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageViewRight.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageViewRight.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.initLayout()

        # 0: 未选中, 1: 左侧选中, 2: 右侧选中
        self.hoveredView = 0
        self.imageViewLeft.enterEvent = self.enterLeft
        self.imageViewLeft.leaveEvent = self.leaveLeft
        self.imageViewRight.enterEvent = self.enterRight
        self.imageViewRight.leaveEvent = self.leaveLeft

    def initLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.splitter)
        
        self.imageViewLeft.setAlignment(Qt.AlignLeft)
        self.imageViewRight.setAlignment(Qt.AlignRight) 

        self.splitter.addWidget(self.imageViewLeft)
        self.splitter.addWidget(self.imageViewRight)

        self.setLayout(layout)

    def setImageByPath(self, path):
        self.imageData = io.imread(path)
        self.manipulatedData = self.imageData.copy()
        pixmap = np2pixmap(self.imageData)
        self.imageSize = pixmap.size()

        self.imageSceneLeft = QGraphicsScene(0, 0, self.imageSize.width(), self.imageSize.height())
        self.imageSceneLeft.addPixmap(pixmap)
        self.imageViewLeft.setScene(self.imageSceneLeft)

        self.imageSceneRight = QGraphicsScene(0, 0, self.imageSize.width(), self.imageSize.height())
        self.imageSceneRight.addPixmap(pixmap)
        self.imageViewRight.setScene(self.imageSceneRight)

    def setImage(self, id):
        path = self.jsonlibrary.getJsonById(id)['imgPath']
        self.setImageByPath(path)

    def update(self):
        difference = np.any(self.imageData != self.manipulatedData, axis=-1)

        # 创建一个红色半透明的图像
        height, width = difference.shape
        result_image = np.zeros((height, width, 4), dtype=np.uint8)
        result_image[difference] = cfg.MASK_COLOR
        # 打开RGB图像和RGBA图像
        rgb_image = Image.fromarray(np.uint8(self.initial_image))
        rgba_image = Image.fromarray(np.uint8(result_image))

        # 将RGBA图像叠加到RGB图像上
        result_image = Image.alpha_composite(rgb_image.convert("RGBA"), rgba_image).convert("RGB")
        # 将图像转换为NumPy数组
        image_array = np.array(result_image)
        self.manipulatedData = image_array.copy()
        pixmap = np2pixmap(image_array)
        self.imageSceneRight.clear()
        self.imageSceneRight.addPixmap(pixmap)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            # 如果按住 Ctrl 键，则执行缩放事件
            delta = event.angleDelta().y() / 120
            factor = 1.1 if delta > 0 else 0.9
            if self.hoveredView == 1:
                self.imageViewLeft.scale(factor, factor)
            elif self.hoveredView == 2:
                self.imageViewRight.scale(factor, factor)
        else:
            # 如果没有按住 Shift 键，则执行默认的滚轮事件
            super().wheelEvent(event)

    def enterLeft(self, event):
        self.hoveredView = 1

    def enterRight(self, event):
        self.hoveredView = 2

    def leaveLeft(self, event):
        self.hoveredView = 0
    
    def mouse_press(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        self.is_mouse_down = True
        
        if self.mode == OperationMode.GLOBAL_RECOGNIZE:
            self.start_pos = (0, 0)
        elif self.mode == OperationMode.ADD_RECT:
            self.start_pos = (x, y)
        elif self.mode == OperationMode.DELETE_RECT:
            self.start_pos = (x, y)
        elif self.mode == OperationMode.MANUAL_ADD:
            self.start_pos = (x, y)
            self.points = [event.scenePos()]
            self.drawing = True

    def mouse_release(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        self.is_mouse_down = False

        if self.mode == OperationMode.GLOBAL_RECOGNIZE:
            self.end_pos = (self.imageSize.width(), self.imageSize.height())
        elif self.mode == OperationMode.ADD_RECT:
            self.end_pos = (x, y)
            self.manipulatedData = self.imageData.copy()
            self.update()
        elif self.mode == OperationMode.DELETE_RECT:
            self.end_pos = (x, y)
            self.manipulatedData = self.imageData.copy()
            self.update()
        elif self.mode == OperationMode.MANUAL_ADD:
            self.end_pos = (x, y)
            self.points.append(event.scenePos())
            self.drawing = False
            self.manipulatedData = self.imageData.copy()
            self.update()
    
    def mouse_move(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()

        if self.mode == OperationMode.GLOBAL_RECOGNIZE:
            self.end_pos = (x, y)
        elif self.mode == OperationMode.ADD_RECT:
            self.end_pos = (x, y)
            self.manipulatedData = self.imageData.copy()
            self.update()
        elif self.mode == OperationMode.DELETE_RECT:
            self.end_pos = (x, y)
            self.manipulatedData = self.imageData.copy()
            self.update()
        elif self.mode == OperationMode.MANUAL_ADD:
            if self.drawing:
                self.points.append(event.scenePos())
                self.manipulatedData = self.imageData.copy()
                self.update()