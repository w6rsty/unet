# -*- coding: utf-8 -*-
from PIL import Image
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor, QBrush, QPainterPath, QPixmap, QPainter, QDesktopServices, QFont
from PyQt5.QtWidgets import QFrame, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF, QUrl, pyqtSignal, QTimer
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime
import os
import subprocess
import sys
import time
import random
from shutil import copyfile
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor, QBrush, QPainterPath, QFont, QIcon
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
import sys
from functools import partial
from docx import Document
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import os
from PyQt5 import QtCore, QtGui, QtWidgets

# 全局变量
image_files = []
dir = r' '  # 用来表示待处理的图像保存路径
files = []
picture = r' '  # 用来表示当前被选择的图片
class_values = []
probability_values = []
preclass_values = []
rstring = ""  # 用于表示显示在label上面的文字（点击预览照片之后）
mingzi = "名字"
nianling = "年龄"

allpx = 652897  # 照片在可缩放画布中的总像素数量
alltext = ""
# 用来提取照片文件的名称
# 可以生成条形图的代码的上界
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def extract_image_name(image_path):
    # 打开图像文件
    with Image.open(image_path) as img:
        # 从图像路径中提取文件名
        image_name_with_extension = os.path.basename(image_path)
        # 去掉文件后缀
        image_name_without_extension = os.path.splitext(image_name_with_extension)[0]
        # 返回文件名
        return image_name_without_extension


class ImageViewer(QGraphicsView):
    textChanged = pyqtSignal(str)  # 定义一个文本改变的信号

    def __init__(self):
        super(ImageViewer, self).__init__()

    def __init__(self):
        super(ImageViewer, self).__init__()

        # 创建场景
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 加载图片
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        # 设置滚轮缩放
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.HighQualityAntialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # 初始化相关变量
        self.drawing = False
        self.rect_item = None
        self.line_item = None
        self.path_item = None
        self.start_point = QPointF()
        self.enable_drawing = False
        self.measuring_distance = False
        self.drawing_path = False
        self.filling_path = False
        self.path = QPainterPath()

    def setDrawingEnabled(self, enabled):
        self.enable_drawing = enabled
        self.measuring_distance = False
        self.drawing_path = False
        self.filling_path = False
        self.removeItems()

    def setMeasuringDistanceEnabled(self, enabled):
        self.measuring_distance = enabled
        self.enable_drawing = False
        self.drawing_path = False
        self.filling_path = False
        self.removeItems()

    def setDrawingPathEnabled(self, enabled):
        self.drawing_path = enabled
        self.enable_drawing = False
        self.measuring_distance = False
        self.filling_path = False
        self.removeItems()

    def setFillingPathEnabled(self, enabled):
        self.filling_path = enabled
        self.enable_drawing = False
        self.measuring_distance = False
        self.drawing_path = False
        self.removeItems()

    def removeItems(self):
        if self.rect_item:
            self.scene.removeItem(self.rect_item)
            self.rect_item = None
        if self.line_item:
            self.scene.removeItem(self.line_item)
            self.line_item = None
        if self.path_item:
            self.scene.removeItem(self.path_item)
            self.path_item = None

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = self.mapToScene(event.pos())
            self.removeItems()
            self.drawing = True
            if self.enable_drawing:
                self.rect_item = self.scene.addRect(QRectF(self.start_point, self.start_point),
                                                    QPen(QColor(255, 0, 0), 3))
            elif self.measuring_distance:
                self.line_item = self.scene.addLine(QLineF(self.start_point, self.start_point),
                                                    QPen(QColor(255, 0, 0), 3))
            elif self.drawing_path or self.filling_path:
                self.path = QPainterPath(self.start_point)
                self.path_item = self.scene.addPath(self.path, QPen(QColor(255, 0, 0), 3))

    def mouseMoveEvent(self, event):
        if self.drawing and event.buttons() & Qt.LeftButton:
            end_point = self.mapToScene(event.pos())
            if self.enable_drawing and self.rect_item:
                rect = QRectF(self.start_point, end_point).normalized()
                self.rect_item.setRect(rect)
            elif self.measuring_distance and self.line_item:
                self.line_item.setLine(QLineF(self.start_point, end_point))
            elif (self.drawing_path or self.filling_path) and self.path_item:
                self.path.lineTo(end_point)
                self.path_item.setPath(self.path)

        super(ImageViewer, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing and event.button() == Qt.LeftButton:
            self.drawing = False
            if self.enable_drawing and self.rect_item:
                # 矩形处理代码
                end_point = self.mapToScene(event.pos())
                rect = QRectF(self.start_point, end_point).normalized()
                self.rect_item.setRect(rect)
                area = rect.width() * rect.height()
                rounded_area = round(area, 2)  # 功能是保留小数点后两位

                text = "{}\n框选矩形的面积为: {:.2f}{}".format(rstring, rounded_area, "px")  # 格式化文本，使患者信息和矩形面积在两行显示
                print("框选矩形的面积为:", text)
                # 发送信号
                self.textChanged.emit(text)

            elif self.measuring_distance and self.line_item:
                # 直线距离处理代码
                end_point = self.mapToScene(event.pos())
                self.line_item.setLine(QLineF(self.start_point, end_point))
                distance = QLineF(self.start_point, end_point).length()
                rounded_distance = round(distance, 2)  # 功能是保留小数点后两位

                text = "{}\n两点之间的直线距离为: {:.2f}{}".format(rstring, rounded_distance,
                                                                   "px")  # 格式化文本，使患者信息和矩形面积在两行显示
                print("两点之间的直线距离为:", text)
                # 发送信号
                self.textChanged.emit(text)

            elif self.drawing_path and self.path_item:
                # 不自动闭合路径
                path_length = self.path.length()
                rounded_path_length = round(path_length, 2)

                text = "{}\n选择路径的长度为: {:.2f}{}".format(rstring, rounded_path_length,
                                                               "px")  # 格式化文本，使患者信息和矩形面积在两行显示
                print("选择路径的长度为:", text)
                # 发送信号
                self.textChanged.emit(text)

            elif self.filling_path and self.path_item:
                # 计算被框选部分的面积
                end_point = self.mapToScene(event.pos())
                self.path.lineTo(end_point)
                self.path.closeSubpath()  # Close the path
                self.path_item.setPath(self.path)
                # area = self.scene.addPath(self.path)
                # 添加路径到场景中，并设置透明的画笔和填充，使路径不可见
                area = self.scene.addPath(self.path, QPen(Qt.NoPen), QBrush(Qt.NoBrush))

                bounding_rect = area.boundingRect()
                area_value = bounding_rect.width() * bounding_rect.height()
                rounded_area_value = round(area_value, 2)

                text = "{}\n框选区域的面积为: {:.2f}{}".format(rstring, rounded_area_value,
                                                               "px")  # 格式化文本，使患者信息和矩形面积在两行显示
                print("框选区域的面积为:", text)

                # 发送信号
                self.textChanged.emit(text)

                QTimer.singleShot(500, self.fillPath)  # 延迟填充路径

    def fillPath(self):
        if self.path_item:
            # 应用填充颜色
            self.path_item.setBrush(QBrush(QColor(255, 200, 200, 128)))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1116, 664)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("QLabel\n"

                           "{\n"
                           "background-color: rgb(221, 221, 221);\n"
                           "\n"
                           "}\n"
                           "")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        # self.ToolButton_2 = QtWidgets.QToolButton(Form)
        self.ToolButton_2 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_2.sizePolicy().hasHeightForWidth())
        self.ToolButton_2.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("历史报告.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_2.setIcon(icon)
        self.ToolButton_2.setIconSize(QtCore.QSize(32, 32))
        # self.ToolButton_2.setIconSize(QtCore.QSize(45, 65))

        self.ToolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_2.setAutoRaise(True)
        self.ToolButton_2.setObjectName("ToolButton_2")
        self.horizontalLayout_5.addWidget(self.ToolButton_2)
        self.ToolButton_10 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_10.sizePolicy().hasHeightForWidth())
        self.ToolButton_10.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("添加图片.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_10.setIcon(icon1)
        self.ToolButton_10.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_10.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_10.setAutoRaise(True)
        self.ToolButton_10.setObjectName("ToolButton_10")
        self.horizontalLayout_5.addWidget(self.ToolButton_10)
        self.ToolButton = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton.sizePolicy().hasHeightForWidth())
        self.ToolButton.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("分级处理.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton.setIcon(icon2)
        self.ToolButton.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton.setAutoRaise(True)
        self.ToolButton.setObjectName("ToolButton")
        self.horizontalLayout_5.addWidget(self.ToolButton)
        self.ToolButton_11 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_11.sizePolicy().hasHeightForWidth())
        self.ToolButton_11.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("保存.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_11.setIcon(icon3)
        self.ToolButton_11.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_11.setAutoRaise(True)
        self.ToolButton_11.setObjectName("ToolButton_11")
        self.horizontalLayout_5.addWidget(self.ToolButton_11)
        self.ToolButton_13 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_13.sizePolicy().hasHeightForWidth())
        self.ToolButton_13.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("另存为.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_13.setIcon(icon4)
        self.ToolButton_13.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_13.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_13.setAutoRaise(True)
        self.ToolButton_13.setObjectName("ToolButton_13")
        self.horizontalLayout_5.addWidget(self.ToolButton_13)
        self.ToolButton_12 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_12.sizePolicy().hasHeightForWidth())
        self.ToolButton_12.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("放大.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_12.setIcon(icon5)
        self.ToolButton_12.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_12.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_12.setAutoRaise(True)
        self.ToolButton_12.setObjectName("ToolButton_12")
        self.horizontalLayout_5.addWidget(self.ToolButton_12)
        self.ToolButton_14 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_14.sizePolicy().hasHeightForWidth())
        self.ToolButton_14.setSizePolicy(sizePolicy)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("缩小.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_14.setIcon(icon6)
        self.ToolButton_14.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_14.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_14.setAutoRaise(True)
        self.ToolButton_14.setObjectName("ToolButton_14")
        self.horizontalLayout_5.addWidget(self.ToolButton_14)
        self.ToolButton_15 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_15.sizePolicy().hasHeightForWidth())
        self.ToolButton_15.setSizePolicy(sizePolicy)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("距离测量.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_15.setIcon(icon7)
        self.ToolButton_15.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_15.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_15.setAutoRaise(True)
        self.ToolButton_15.setObjectName("ToolButton_15")
        self.horizontalLayout_5.addWidget(self.ToolButton_15)
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("曲线标注.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon8)
        self.toolButton_2.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_5.addWidget(self.toolButton_2)
        self.toolButton_3 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("矩形.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon9)
        self.toolButton_3.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_3.setAutoRaise(True)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_5.addWidget(self.toolButton_3)
        self.ToolButton_6 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_6.sizePolicy().hasHeightForWidth())
        self.ToolButton_6.setSizePolicy(sizePolicy)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("任意框选.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_6.setIcon(icon10)
        self.ToolButton_6.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_6.setAutoRaise(True)
        self.ToolButton_6.setObjectName("ToolButton_6")
        self.horizontalLayout_5.addWidget(self.ToolButton_6)
        self.ToolButton_5 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_5.sizePolicy().hasHeightForWidth())
        self.ToolButton_5.setSizePolicy(sizePolicy)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("重置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_5.setIcon(icon11)
        self.ToolButton_5.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_5.setShortcut("")
        self.ToolButton_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_5.setAutoRaise(True)
        self.ToolButton_5.setObjectName("ToolButton_5")
        # self.horizontalLayout_5.addWidget(self.ToolButton_5)
        self.toolButton_4 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_4.sizePolicy().hasHeightForWidth())
        self.toolButton_4.setSizePolicy(sizePolicy)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("模板更改.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon12)
        self.toolButton_4.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_4.setAutoRaise(True)
        self.toolButton_4.setObjectName("toolButton_4")
        # self.horizontalLayout_5.addWidget(self.toolButton_4)
        self.ToolButton_8 = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolButton_8.sizePolicy().hasHeightForWidth())
        self.ToolButton_8.setSizePolicy(sizePolicy)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_8.setIcon(icon13)
        self.ToolButton_8.setIconSize(QtCore.QSize(32, 32))
        self.ToolButton_8.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ToolButton_8.setAutoRaise(True)
        self.ToolButton_8.setObjectName("ToolButton_8")
        # self.horizontalLayout_5.addWidget(self.ToolButton_8)
        self.toolButton = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("帮助.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon14)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_5.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.SimpleCardWidget = SimpleCardWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SimpleCardWidget.sizePolicy().hasHeightForWidth())
        self.SimpleCardWidget.setSizePolicy(sizePolicy)
        self.SimpleCardWidget.setObjectName("SimpleCardWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.SimpleCardWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.SimpleCardWidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2.addWidget(self.frame_2)
        # 到此frame_2已经创建完成，接下来对其内部进行布局，这个代码实现的是滚动鼠标缩放图片
        # 创建 ImageViewer 实例
        self.image_viewer = ImageViewer()

        # 设置垂直布局
        self.vertical_layout = QtWidgets.QVBoxLayout(self.frame_2)
        self.vertical_layout.addWidget(self.image_viewer)
        # 将margin和spacing设置为0
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        # 设置 QFrame 属性
        self.frame_2.setFrameStyle(QFrame.Box)
        self.frame_2.setLineWidth(1)
        # self.frame_2.setLayout(self.vertical_layout)
        # 加载图片
        image_path = r'photos\IDRiD_038.jpg'
        pixmap = QPixmap(image_path)

        # 设置照片显示的最大尺寸
        max_width = 1000
        max_height = 800

        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)

        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)
        # 滚动鼠标缩放图片的功能到此为止

        self.frame1 = QtWidgets.QFrame(self.SimpleCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame1.sizePolicy().hasHeightForWidth())
        self.frame1.setSizePolicy(sizePolicy)
        self.frame1.setObjectName("frame1")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.SubtitleLabel_3 = SubtitleLabel(self.frame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SubtitleLabel_3.sizePolicy().hasHeightForWidth())
        self.SubtitleLabel_3.setSizePolicy(sizePolicy)
        #         self.SubtitleLabel_3.setStyleSheet("font: 9pt \"楷体\";\n"
        # "font: 9pt \"黑体\";")

        self.SubtitleLabel_3.setStyleSheet("font: 14pt \"楷体\";\n"
                                           "font: 16pt \"黑体\";")

        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.horizontalLayout_14.addWidget(self.SubtitleLabel_3)
        self.IndeterminateProgressBar = IndeterminateProgressBar(self.frame1)
        self.IndeterminateProgressBar.setObjectName("IndeterminateProgressBar")
        self.horizontalLayout_14.addWidget(self.IndeterminateProgressBar)
        self.verticalLayout_2.addWidget(self.frame1)
        self.horizontalLayout.addWidget(self.SimpleCardWidget)
        spacerItem1 = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.SimpleCardWidget_2 = SimpleCardWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SimpleCardWidget_2.sizePolicy().hasHeightForWidth())
        self.SimpleCardWidget_2.setSizePolicy(sizePolicy)
        self.SimpleCardWidget_2.setStyleSheet("QLabel\n"
                                              "{\n"
                                              "\n"
                                              "background-color: rgb(220, 220, 220);\n"
                                              "\n"
                                              "}\n"
                                              "")
        self.SimpleCardWidget_2.setObjectName("SimpleCardWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.SimpleCardWidget_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalFrame = QtWidgets.QFrame(self.SimpleCardWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.verticalFrame.sizePolicy().hasHeightForWidth())
        self.verticalFrame.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(199, 199, 199))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(199, 199, 199))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(199, 199, 199))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(199, 199, 199))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.verticalFrame.setPalette(palette)
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.line_6 = QtWidgets.QFrame(self.verticalFrame)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_8.addWidget(self.line_6)
        self.gridFrame = QtWidgets.QFrame(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.BodyLabel_3 = BodyLabel(self.gridFrame)
        self.BodyLabel_3.setStyleSheet("")
        self.BodyLabel_3.setText("")
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.gridLayout.addWidget(self.BodyLabel_3, 0, 2, 1, 1)
        self.BodyLabel_5 = BodyLabel(self.gridFrame)
        self.BodyLabel_5.setStyleSheet("")
        self.BodyLabel_5.setText("")
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.gridLayout.addWidget(self.BodyLabel_5, 0, 1, 1, 1)
        self.BodyLabel_7 = BodyLabel(self.gridFrame)
        self.BodyLabel_7.setStyleSheet("")
        self.BodyLabel_7.setText("")
        self.BodyLabel_7.setObjectName("BodyLabel_7")
        self.gridLayout.addWidget(self.BodyLabel_7, 2, 1, 1, 1)
        self.verticalFrame1 = QtWidgets.QFrame(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalFrame1.sizePolicy().hasHeightForWidth())
        self.verticalFrame1.setSizePolicy(sizePolicy)
        self.verticalFrame1.setStyleSheet("border: 1px solid grey;")
        self.verticalFrame1.setObjectName("verticalFrame1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalFrame1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.toolButton_5 = QtWidgets.QToolButton(self.verticalFrame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_5.sizePolicy().hasHeightForWidth())
        self.toolButton_5.setSizePolicy(sizePolicy)
        self.toolButton_5.setStyleSheet("font: 16pt \"黑体\";\n"
                                        "border: px solid grey;")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("加号.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton_5.setIcon(icon15)
        self.toolButton_5.setIconSize(QtCore.QSize(35, 35))
        self.toolButton_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_5.setAutoRaise(False)
        self.toolButton_5.setObjectName("toolButton_5")
        self.verticalLayout_6.addWidget(self.toolButton_5, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.verticalFrame1, 2, 2, 1, 1)
        self.BodyLabel_4 = BodyLabel(self.gridFrame)
        self.BodyLabel_4.setStyleSheet("")
        self.BodyLabel_4.setText("")
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.gridLayout.addWidget(self.BodyLabel_4, 0, 0, 1, 1)
        self.BodyLabel_6 = BodyLabel(self.gridFrame)
        self.BodyLabel_6.setStyleSheet("")
        self.BodyLabel_6.setText("")
        self.BodyLabel_6.setObjectName("BodyLabel_6")
        self.gridLayout.addWidget(self.BodyLabel_6, 2, 0, 1, 1)
        self.verticalLayout_8.addWidget(self.gridFrame)
        self.line = QtWidgets.QFrame(self.verticalFrame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_8.addWidget(self.line)
        self.BodyLabel = BodyLabel(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.BodyLabel.sizePolicy().hasHeightForWidth())
        self.BodyLabel.setSizePolicy(sizePolicy)
        self.BodyLabel.setText("")
        self.BodyLabel.setObjectName("BodyLabel")
        self.verticalLayout_8.addWidget(self.BodyLabel)
        self.BodyLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        self.BodyLabel_9 = BodyLabel(self.verticalFrame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 159, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.BodyLabel_9.setPalette(palette)
        self.BodyLabel_9.setStyleSheet("\n"
                                       "QLabel\n"
                                       "{\n"
                                       "font: 20pt \"黑体\";\n"
                                       "border-radius: 50px;\n"
                                       "border: 2px solid grey;\n"
                                       # "background-color: rgb(0, 159, 170);\n"
                                       "background-color: rgba(128, 128, 128, 100);\n"
                                       "color: black;\n"
                                       "\n"
                                       "}\n"
                                       "")

        self.BodyLabel_9.setAlignment(QtCore.Qt.AlignCenter)
        self.BodyLabel_9.setObjectName("BodyLabel_9")
        self.verticalLayout_8.addWidget(self.BodyLabel_9)

        self.text_edit = QTextEdit(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.text_edit.sizePolicy().hasHeightForWidth())
        self.text_edit.setSizePolicy(sizePolicy)
        self.text_edit.setText("")
        self.text_edit.setObjectName("text_edit")
        self.verticalLayout_8.addWidget(self.text_edit)

        self.verticalLayout_3.addWidget(self.verticalFrame)
        self.line_4 = QtWidgets.QFrame(self.SimpleCardWidget_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)
        self.PrimaryPushButton = PrimaryPushButton(self.SimpleCardWidget_2)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.verticalLayout_3.addWidget(self.PrimaryPushButton)
        # self.PrimaryPushButton.setStyleSheet("background-color: rgba(128, 128, 128, 100);\n""color: black;\n"  )
        # style_sheet = """
        #     QPushButton {
        #         font: 20pt "黑体";
        #         border-radius: 50px;
        #         border: 2px solid grey;
        #         background-color: rgba(128, 128, 128, 100);
        #         color: black;
        #     }
        # """
        # self.PrimaryPushButton.setStyleSheet(style_sheet)

        # style_sheet = """
        #     QPushButton {
        #         font: 20pt "黑体";
        #         border-radius: 500px; /* 设置圆角边框 */
        #         border: 2px solid grey;
        #         background-color: rgba(128, 128, 128, 100);
        #         color: black;
        #     }
        # """
        # self.PrimaryPushButton.setStyleSheet(style_sheet)
        style_sheet1 = """
            QPushButton {
                font: 20pt "黑体";
                border-radius: 10px; /* 轻微的圆角，形成钝角效果 */
                border: 2px solid grey;
                background-color: rgba(128, 128, 128, 100);
                color: black;
            }
        """
        self.PrimaryPushButton.setStyleSheet(style_sheet1)

        self.horizontalLayout.addWidget(self.SimpleCardWidget_2)
        spacerItem2 = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame)
        # 预览最后面的加号用来添加文件
        self.toolButton_5.clicked.connect(self.select_photos_and_append)

        # pushbuttom生成word报告，参数解释：第一个参数是调用的函数，第二个参数是报告底版的文件路径，第三个参数是需要替换图片的图片路径(这个参数很可能要更换成全局变量，来进行传参），第三个参数是患者报告要集中保存的文件夹
        # self.PrimaryPushButton.clicked.connect(
        #     partial(self.replace_images, "数码宝贝.docx", r"C:\Users\cyq\Desktop\new\photos\曾东华0 OS_006.jpg",
        #             r'C:\Users\cyq\Desktop\new\报告单文件夹'))
        # self.PrimaryPushButton.clicked.connect(
        #     partial(self.replace_images, r"C:\Users\cyq\Desktop\new\数码宝贝.docx",
        #             r"C:\Users\cyq\Desktop\new\photos\曾东华0 OS_006.jpg",
        #             r'C:\Users\cyq\Desktop\new\报告单文件夹'))
        self.PrimaryPushButton.clicked.connect(
            partial(self.replace_images, r"assets\糖尿病视网膜诊断报告模板.docx",
                    r'报告单文件夹'))
        self.BodyLabel_4.mousePressEvent = self.on_label1_clicked  # 设置点击事件处理函数（预览的第一张图片）
        self.BodyLabel_5.mousePressEvent = self.on_label2_clicked  # 设置点击事件处理函数（预览的第二张图片）
        self.BodyLabel_3.mousePressEvent = self.on_label3_clicked  # 设置点击事件处理函数（预览的第一张图片）
        self.BodyLabel_6.mousePressEvent = self.on_label4_clicked  # 设置点击事件处理函数（预览的第一张图片）
        self.BodyLabel_7.mousePressEvent = self.on_label5_clicked  # 设置点击事件处理函数（预览的第一张图片）

        # 用来生成相应的条形图上界
        self.BodyLabel_9.mousePressEvent = self.on_label9_clicked  # 设置点击事件处理函数（预览的第一张图片）
        # 用来生成相应的条形图下界

        # 用来实现获取矩形和直线的面积和长度

        # self.toolButton_3.clicked.connect(lambda: self.image_viewer.setDrawingEnabled(True))#用来画矩形框
        # self.ToolButton_6.clicked.connect(lambda: self.image_viewer.setDrawingEnabled(False))#用来撤销所有功能
        # self.toolButton_2.clicked.connect(lambda: self.image_viewer.setMeasuringDistanceEnabled(True))#用来画直线
        self.toolButton_3.clicked.connect(lambda: self.image_viewer.setDrawingEnabled(True))  # 矩形框选
        self.ToolButton_5.clicked.connect(lambda: self.image_viewer.setDrawingEnabled(False))  # 撤销操作
        self.ToolButton_15.clicked.connect(lambda: self.image_viewer.setMeasuringDistanceEnabled(True))  # 测量直线距离
        self.toolButton_2.clicked.connect(lambda: self.image_viewer.setDrawingPathEnabled(True))  # 曲线标注
        self.ToolButton_6.clicked.connect(lambda: self.image_viewer.setFillingPathEnabled(True))  # 随机区域填充
        # 控件：查看历史报告/暂时被我改为了显示动态条形图
        # self.ToolButton_2.clicked.connect(self.file_openFolder)
        self.ToolButton_2.clicked.connect(self.file_openFolder)
        # 控件：查看图片
        self.ToolButton_10.clicked.connect(self.images_openFolder)
        # 控件：保存
        self.ToolButton_11.clicked.connect(self.save0_image)
        # 控件：另存为
        self.ToolButton_13.clicked.connect(self.save_image)
        # 控件：帮助，网页跳转
        self.toolButton.clicked.connect(self.open_webpage)
        # 控件：模型更改
        self.toolButton_4.clicked.connect(self.open_word_file)
        # 控件：设置 白天夜间模式切换：初始化为白天模式
        self.isDayMode = True
        self.ToolButton_8.clicked.connect(self.toggleMode)

        # 控件：点击可以放大照片
        self.ToolButton_12.clicked.connect(self.zoom_in_image)
        # 控件：点击可以缩小照片
        self.ToolButton_14.clicked.connect(self.zoom_out_image)
        # 控件：点击可以进行预测
        self.ToolButton.clicked.connect(self.getPredictData)
        # 将信号连接到槽函数
        self.image_viewer.textChanged.connect(self.updateBodyLabel)

        self.retranslateUi(Form)
        # self.showImage(self.BodyLabel_4, r'C:\Users\cyq\Desktop\new\photos\吴素平0 OS_005.jpg')

        self.pre_showImage()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def file_openFolder(self):  # 用来查看历史报告
        # folder_path = r'C:\Users\cyq\Desktop\new\报告单文件夹'
        folder_path = r"assets\报告单文件夹"
        os.startfile(folder_path)

    # def file_openFolder(self):  # 用来查看历史报告/暂时被我改成了动态条形图
    #     try:
    #         subprocess.run(["python", "bar_stop_start.py"])
    #     except FileNotFoundError:
    #         print("Error: The specified Python file could not be found.")

    def images_openFolder(self):  # 用来查看历史图片
        # folder_path = r'C:\Users\cyq\Desktop\new\photos'
        folder_path = "assets\save"
        os.startfile(folder_path)

    def zoom_in_image(self):
        # 放大图片的方法
        factor = 1.2  # 定义放大的倍数
        self.image_viewer.scale(factor, factor)

    def zoom_out_image(self):
        # 缩小图片的方法
        factor = 1.2
        self.image_viewer.scale(1.0 / factor, 1.0 / factor)

    def toggleMode(self):
        # 根据当前模式切换
        if self.isDayMode:
            self.setNightMode()
        else:
            self.setDayMode()

        # 更新模式标志
        self.isDayMode = not self.isDayMode

    # def setDayMode(self):
    #     # 设置白天模式的样式
    #     Form.setStyleSheet("")  # 清除样式表

    #     # # 更新标签显示
    #     # self.label.setText("当前模式：白天模式")

    # def setNightMode(self):
    #     # 设置夜间模式的样式
    #     Form.setStyleSheet("background-color: lightgrey; color: white;")

        # # 更新标签显示
        # self.label.setText("当前模式：夜间模式")

    # 以上是白天夜间模式切换
    def open_word_file(self):  # 用它打开特定文件（模板）的函数
        # 指定 Word 文件的路径
        # word_file_path = r'C:\Users\cyq\Desktop\new\数码宝贝.docx'  # 请替换为实际的文件路径
        word_file_path = r'报告样板.docx'  # 请替换为实际的文件路径
        # 将文件路径转换为 QUrl
        url = QUrl.fromLocalFile(word_file_path)

        # 使用 QDesktopServices 打开 Word 文件
        QDesktopServices.openUrl(url)

    def open_webpage(self):  # 用于打开特定网页的函数
        # 打开网页的 URL
        url = QUrl('https://www.xzsdyyy.com/department/')

        # 使用 QDesktopServices 打开网页
        QDesktopServices.openUrl(url)

    def save0_image(self):  # 用于保存的函数

        # target0_folder = r'C:\Users\cyq\Desktop\new\用于保存'
        target0_folder = r"assets\save"
        photo_filename0 = os.path.basename(picture)
        # 构建目标文件路径
        target_file_path = os.path.join(target0_folder, photo_filename0)
        # 复制照片到目标文件夹
        copyfile(picture, target_file_path)
        print("图片已保存")

    def save_image(self):  # 用于另存为的函数

        # 获取用户选择保存的路径
        base_name = os.path.splitext(os.path.basename(picture))[0]
        print(base_name)
        save_path, _ = QFileDialog.getSaveFileName(None, '保存图片', base_name, 'Images (*.png *.jpg *.bmp)')
        print(base_name)

        # 检查保存路径是否为空
        if save_path:
            # 使用 QPixmap 保存图片
            pixmap = QPixmap(picture)
            pixmap.save(save_path)
            print(f'图片已另存为 {save_path}')

    def pre_showImage(self):  # 这是用来预览部分显示的函数
        global dir
        # 显示指定文件夹的图片：前5张图片
        # dir = r"C:\Users\cyq\Desktop\new\photos"
        dir = r"assets\xueguan_pre_photos"
        # 获取文件夹中的所有文件
        global files
        files = os.listdir(dir)
        print(files)
        global image_files
        # 取前5张图片
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))][:12]
        print(image_files)
        if len(image_files) > 0:
            self.showImage(self.BodyLabel_4, os.path.join(dir, image_files[0]))
            print(os.path.join(dir, image_files[0]))
        if len(image_files) > 1:
            self.showImage(self.BodyLabel_5, os.path.join(dir, image_files[1]))
        if len(image_files) > 2:
            self.showImage(self.BodyLabel_3, os.path.join(dir, image_files[2]))
        if len(image_files) > 3:
            self.showImage(self.BodyLabel_6, os.path.join(dir, image_files[3]))
        if len(image_files) > 4:
            self.showImage(self.BodyLabel_7, os.path.join(dir, image_files[4]))

    # 用来删除指定文件夹里面的第一个文件
    def delete_first_photo(self):
        # 用来删除被点击的图片picture
        if os.path.exists(picture):
            os.remove(picture)
            print(f"Deleted: {picture}")
        else:
            print(f"Photo not found: {picture}")

    def showImage(self, target_label, file_path):
        # 显示选择的图片在目标标签上
        pixmap = QtGui.QPixmap(file_path)

        # 设置标签的最大宽度和高度
        max_width = 200
        max_height = 200
        target_label.setMaximumSize(max_width, max_height)

        # 缩放图片以适应标签大小
        scaled_pixmap = pixmap.scaledToWidth(max_width)
        target_label.setPixmap(scaled_pixmap)
        target_label.setScaledContents(True)  # 使图片适应标签大小

    def select_photos_and_append(self):
        # 删除已经预览的那张照片
        self.delete_first_photo()
        # 弹出文件选择对话框
        photo_paths, _ = QFileDialog.getOpenFileNames(None, '选择照片',
                                                      filter="Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        if photo_paths:
            # 目标文件夹
            target_folder = r'photos'  # 请替换为你的目标文件夹路径
            target_folder = r'photos'  # 请替换为你的目标文件夹路径
            # 遍历选择的照片路径
            for photo_path in photo_paths:
                # 获取照片文件名
                photo_filename = os.path.basename(photo_path)

                # 构建目标文件路径
                target_file_path = os.path.join(target_folder, photo_filename)

                # 复制照片到目标文件夹
                copyfile(photo_path, target_file_path)

            print('照片追加完成')
        global image_files
        # 取前7张图片，至少五张
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))][:7]

        self.pre_showImage()

    def find_image_paths(self, doc):
        image_paths = []
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                image_paths.append(rel.target_ref)
        print(image_paths)
        return image_paths

    # def replace_images(self, doc_path, file_path):
    #     # 打开 Word 文档
    #     doc = Document(doc_path)
    #     self.find_image_paths(doc)
    #     # 获取当前日期
    #     print(picture)
    #     new_image_path = picture
    #     current_date = datetime.now().strftime("%Y年%m月%d日")
    #     # 遍历文档中的所有图片
    #     for rel in doc.part.rels.values():
    #         if "image" in rel.reltype:
    #             image_path = os.path.join(os.path.dirname(doc_path), rel.target_ref)
    #             print(image_path)
    #             print(f"Original Image Path: {image_path}")

    #             # 替换图片
    #             if os.path.exists(new_image_path) and image_path == 'media/image1.jpeg':
    #                 rel.target_part._blob = open(new_image_path, 'rb').read()
    #                 print(f"Image replaced with: {new_image_path}")
    #             else:
    #                 print(f"New image path does not exist: {new_image_path}")
    #     # 遍历文档中的所有段落和运行
    #     for paragraph in doc.paragraphs:
    #         for run1 in paragraph.runs:
    #             if run1.text:
    #                 if 'A' in run1.text:
    #                     run1.text = run1.text.replace('A', mingzi)

    #                 if 'B' in run1.text:
    #                     run1.text = run1.text.replace('B', "男")
    #                 if 'C' in run1.text:
    #                     run1.text = run1.text.replace('C', nianling)
    #                 if 'D' in run1.text:
    #                     run1.text = run1.text.replace('D', "033")
    #                 if 'E' in run1.text:
    #                     run1.text = run1.text.replace('E', "045")
    #                 if 'F' in run1.text:
    #                     run1.text = run1.text.replace('F', "眼科")
    #                 if 'G' in run1.text:
    #                     run1.text = run1.text.replace('G', "452")
    #                 if 'H' in run1.text:
    #                     run1.text = run1.text.replace('H', "糖尿病引起的眼底病变")

    #                 # 使用 if 语句进行条件替换
    #                 if 'a' in run1.text:
    #                     run1.text = run1.text.replace('a',
    #                                                   '糖尿病性视网膜病变，微血管轻微出血。')
    #                 if 'b' in run1.text:
    #                     run1.text = run1.text.replace('b',
    #                                                   f"糖网分级共为五级，Class: {class_values}, 您的分级概率为，Probability: {probability_values}, 您的最大概率为，Prediction: {preclass_values} \n您平时需要特别注意以下几点，并且按照医生的建议进行治疗和药物管理：1.控制血糖平衡 2.定期眼科检查 3.戒烟限酒，减少并发症的风险。 \n建议您服用的药物有：1.口服类降糖药，如二甲双胍、磺脲类药物等，用于帮助控制血糖水平 2.抗高血压药物，如ACE抑制剂、ARBs等，用于控制高血压 \n注：具体用药规则请谨遵医嘱。")
    #                 # 替换 'time' 为当前日期
    #                 if 'time' in run1.text:
    #                     run1.text = run1.text.replace('time', current_date)

        output_folder = "assets\糖尿病视网膜检测报告"  # 替换为你的目标文件夹路径
        new_doc_path = os.path.join(output_folder,
                                    os.path.splitext(os.path.basename(new_image_path))[0] + "_modified.docx")
        print(os.path.splitext(os.path.basename(doc_path))[0])
        print()
        doc.save(new_doc_path)  # 文件保存在指定文件夹下

    #     print(f"Modified document saved at: {new_doc_path}")
    #     try:
    #         if sys.platform == 'win32':
    #             os.startfile(new_doc_path)
    #         elif sys.platform == 'darwin':
    #             subprocess.Popen(['open', new_doc_path])
    #         else:
    #             subprocess.Popen(['xdg-open', new_doc_path])
    #     except Exception as e:
    #         print(f"Error opening the document: {e}")

    #     self.pre_showImage()

    def on_label9_clicked(self, event):
        try:
            # 传递参数给 bar_stop_start.py
            parameters = [0.1, 0.4, 0.4, 0.25, 0.8]
            parameters = probability_values
            subprocess.run(["python", "bar_gra_2.py"] + [str(param) for param in parameters])
        except FileNotFoundError:
            print("Error: The specified Python file could not be found.")

    def on_label1_clicked(self, event):

        # 加载图片
        pixmap = QtGui.QPixmap(os.path.join(dir, image_files[0]))
        print(os.path.join(dir, image_files[0]))

        # 全局变量 用来表示当前被选中的图像
        global picture
        picture = os.path.join(dir, image_files[0])

        # 设置照片显示的最大尺寸
        max_width = 1200
        max_height = 900

        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)

        # 用来显示信息在label上面
        ex_image_name = extract_image_name(picture)  # 获得照片的名称
        fields = ex_image_name.split("_")  # 将照片名称字符串按照"_"进行划分
        print(fields)
        global rstring
        rstring = "姓名: {} 年龄：{} 病变区域：{}".format(fields[1], fields[2], fields[3])

        global mingzi
        mingzi = fields[1]
        global nianling
        nianling = fields[2]

        self.BodyLabel.setText(rstring)
        # 样式表设置
        # style_sheet = "QLabel { color: black; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        style_sheet = "QLabel {background-color: rgba(0, 0, 0, 0); color: black ; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"

        self.BodyLabel.setStyleSheet(style_sheet)
    def on_label2_clicked(self, event):

        pixmap = QtGui.QPixmap(os.path.join(dir, image_files[1]))
        print(os.path.join(dir, image_files[1]))
        # 全局变量 用来表示当前被选中的图像
        global picture
        picture = os.path.join(dir, image_files[1])

        # # 设置照片显示的最大尺寸
        # max_width = 1000
        # max_height = 800

        # 设置照片显示的最大尺寸
        max_width = 1200
        max_height = 900

        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)

        # 用来显示信息在label上面
        ex_image_name = extract_image_name(picture)  # 获得照片的名称
        fields = ex_image_name.split("_")  # 将照片名称字符串按照"_"进行划分
        print(fields)
        global rstring
        rstring = "姓名: {} 年龄：{} 病变区域：{}".format(fields[1], fields[2], fields[3])

        global mingzi
        mingzi = fields[1]
        global nianling
        nianling = fields[2]

        self.BodyLabel.setText(rstring)
        # 样式表设置
        # self.BodyLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        style_sheet = "QLabel {background-color: rgba(0, 0, 0, 0); color: black ; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        self.BodyLabel.setStyleSheet(style_sheet)

    def on_label3_clicked(self, event):

        # 加载图片
        pixmap = QtGui.QPixmap(os.path.join(dir, image_files[2]))
        print(os.path.join(dir, image_files[2]))

        # 全局变量 用来表示当前被选中的图像
        global picture
        picture = os.path.join(dir, image_files[2])
        # # 设置照片显示的最大尺寸
        # max_width = 1000
        # max_height = 800

        # 设置照片显示的最大尺寸
        max_width = 1200
        max_height = 900

        print("picture是" + picture)
        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)

        # 用来显示信息在label上面
        ex_image_name = extract_image_name(picture)  # 获得照片的名称
        fields = ex_image_name.split("_")  # 将照片名称字符串按照"_"进行划分
        print(fields)
        global rstring
        rstring = "姓名: {} 年龄：{} 病变区域：{}".format(fields[1], fields[2], fields[3])

        global mingzi
        mingzi = fields[1]
        global nianling
        nianling = fields[2]

        self.BodyLabel.setText(rstring)
        # 样式表设置
        # style_sheet = "QLabel { color: black; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        style_sheet = "QLabel {background-color: rgba(0, 0, 0, 0); color: black ; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"

        self.BodyLabel.setStyleSheet(style_sheet)

    def on_label4_clicked(self, event):

        # 加载图片
        pixmap = QtGui.QPixmap(os.path.join(dir, image_files[3]))
        print(os.path.join(dir, image_files[3]))

        # 全局变量 用来表示当前被选中的图像
        global picture
        picture = os.path.join(dir, image_files[3])
        # # 设置照片显示的最大尺寸
        # max_width = 1000
        # max_height = 800

        # 设置照片显示的最大尺寸
        max_width = 1200
        max_height = 900

        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)

        # 用来显示信息在label上面
        ex_image_name = extract_image_name(picture)  # 获得照片的名称
        fields = ex_image_name.split("_")  # 将照片名称字符串按照"_"进行划分
        print(fields)
        global rstring
        rstring = "姓名: {} 年龄：{} 病变区域：{}".format(fields[1], fields[2], fields[3])

        global mingzi
        mingzi = fields[1]
        global nianling
        nianling = fields[2]

        self.BodyLabel.setText(rstring)
        # 样式表设置
        # style_sheet = "QLabel { color: black; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        style_sheet = "QLabel {background-color: rgba(0, 0, 0, 0); color: black ; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"

        self.BodyLabel.setStyleSheet(style_sheet)

    def on_label5_clicked(self, event):

        # 加载图片
        pixmap = QtGui.QPixmap(os.path.join(dir, image_files[4]))
        print(os.path.join(dir, image_files[4]))

        # 全局变量 用来表示当前被选中的图像
        global picture
        picture = os.path.join(dir, image_files[4])
        # # 设置照片显示的最大尺寸
        # max_width = 1000
        # max_height = 800

        # 设置照片显示的最大尺寸
        max_width = 1200
        max_height = 900

        # 缩放照片以适应最大尺寸
        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
        # 将缩放后的照片设置给 QGraphicsPixmapItem
        self.image_viewer.image_item.setPixmap(scaled_pixmap)

        # 用来显示信息在label上面
        ex_image_name = extract_image_name(picture)  # 获得照片的名称
        fields = ex_image_name.split("_")  # 将照片名称字符串按照"_"进行划分
        print(fields)
        global rstring
        rstring = "姓名: {} 年龄：{} 病变区域：{}".format(fields[1], fields[2], fields[3])

        global mingzi
        mingzi = fields[1]
        global nianling
        nianling = fields[2]

        self.BodyLabel.setText(rstring)
        # 样式表设置
        # style_sheet = "QLabel { color: black; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        style_sheet = "QLabel {background-color: rgba(0, 0, 0, 0); color: black ; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"

        self.BodyLabel.setStyleSheet(style_sheet)

    def yuce(self):
        global class_values, probability_values, preclass_values
        start_time = time.time()
        # image_file = 'IDRiD_003.jpg'
        # image_path = 'E:/糖网/11/11/retfound-web/src/image/' + image_file  # 保存路径需要根据你的实际需求修改
        global picture
        image_path = picture  # 保存路径需要根据你的实际需求修改
        print(image_path)
        # 构建预测命令
        # command = f'python E:/糖网/11/11/1.py --eval --image_path={image_path}'
        # command = f'python E:/糖网/11/11/1.py --eval --image_path={image_path}'
        command = f'python src/pages/model_2/1.py --eval --image_path={image_path}'
        print('Command:', command)  # 打印检查命令是否正确
        result = subprocess.getoutput(command)
        print(result)
        print('json ok')
        # command = f'python E:/糖网/11/11/1.py --eval --image_path={picture}'
        # print('Command:', command)  # 打印检查命令是否正确
        # result = subprocess.getoutput(command)
        # print(result)
        # print('json ok')
        # 解析预测结果
        # 这里需要根据你的预测代码的输出格式进行解析
        # 假设预测结果的格式为 "Class {class_idx}: Probability {probability:.4f}" 和 "该图片最有可能分级是 {preclass}"
        class_values, probability_values, preclass_values = self.extract_values_from_output(result)
        print(class_values, probability_values, preclass_values)
        # print(class_values)
        end_time = time.time()
        # 计算执行时间
        execution_time = end_time - start_time
        print(f"Predict executed in {execution_time} seconds")
        self.text_edit.setText(
            f"糖网分级共为五级，Class: {class_values}, 您的分级概率为，Probability: {probability_values}, 您的最大概率为，Prediction: {preclass_values} \n您平时需要特别注意以下几点，并且按照医生的建议进行治疗和药物管理：1.控制血糖平衡 2.定期眼科检查 3.戒烟限酒，减少并发症的风险。 \n建议您服用的药物有：1.口服类降糖药，如二甲双胍、磺脲类药物等，用于帮助控制血糖水平 2.抗高血压药物，如ACE抑制剂、ARBs等，用于控制高血压 \n注：具体用药规则请谨遵医嘱。")
        style_sheet = "QTextEdit { color: black; font-size: 20px; font-family: Arial; }"
        self.text_edit.setStyleSheet(style_sheet)

        return class_values, probability_values, preclass_values

    # 槽函数用于更新 BodyLabel 的文本内容
    def updateBodyLabel(self, text):
        self.BodyLabel.setText(text)
        # 样式表设置

        style_sheet = "QLabel { background-color: rgba(0, 0, 0, 0); color: black; font-size: 31px; font-family: Arial; font-weight: bold; text-align: center; }"
        self.BodyLabel.setStyleSheet(style_sheet)

    def extract_values_from_output(self, result):
        start_time = time.time()
        lines = result.split('\n')  # 将字符串按行分割成列表
        class_values = []
        probability_values = []
        preclass_values = []

        for line in lines:
            if 'Class:' in line:
                try:
                    class_idx_parts = line.split('Class:')
                    class_idx = int(class_idx_parts[1].split(' ')[0].strip())  # 提取Class的值
                    probability = float(line.split('Probability:')[1].strip())  # 提取Probability的值
                    class_values.append(class_idx)
                    probability_values.append(probability)
                except ValueError as e:
                    print(f"Error parsing class or probability: {e}")
            elif 'preclass:' in line:
                try:
                    preclass_parts = line.split('preclass:[')
                    preclass = int(preclass_parts[1].split(']')[0].strip())  # 提取preclass的值
                    preclass_values.append(preclass)
                except ValueError as e:
                    print(f"Error parsing preclass: {e}")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"EXT executed in {execution_time} seconds")
        return class_values, probability_values, preclass_values

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "糖尿病视网膜病变分级"))
        font1 = QFont()
        font1.setPointSize(14)  # 设置字体大小为16
        font1.setFamily("黑体")  # 设置字体为宋体
        self.ToolButton_2.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_2.setText(_translate("Form", "历史数据"))

        self.ToolButton_10.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_10.setText(_translate("Form", "查看图片"))

        self.ToolButton.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton.setText(_translate("Form", "分级处理"))

        self.ToolButton_11.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_11.setText(_translate("Form", "保存"))

        self.ToolButton_13.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_13.setText(_translate("Form", "另存为"))

        self.ToolButton_12.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_12.setText(_translate("Form", "图片放大"))

        self.ToolButton_14.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_14.setText(_translate("Form", "图片缩小"))

        self.ToolButton_15.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_15.setText(_translate("Form", "距离测量"))

        self.toolButton_2.setFont(font1)  # 将设置后的字体应用到按钮上
        self.toolButton_2.setText(_translate("Form", "曲线标注"))

        self.toolButton_3.setFont(font1)  # 将设置后的字体应用到按钮上
        self.toolButton_3.setText(_translate("Form", "矩形框选"))

        self.ToolButton_6.setFont(font1)  # 将设置后的字体应用到按钮上
        self.ToolButton_6.setText(_translate("Form", "任意框选"))

        # self.ToolButton_5.setFont(font1)  # 将设置后的字体应用到按钮上
        # self.ToolButton_5.setText(_translate("Form", "重置"))

        # self.toolButton_4.setFont(font1)  # 将设置后的字体应用到按钮上
        # self.toolButton_4.setText(_translate("Form", "模板更改"))

        # self.ToolButton_8.setFont(font1)  # 将设置后的字体应用到按钮上
        # self.ToolButton_8.setText(_translate("Form", "模式更换"))

        self.toolButton.setFont(font1)  # 将设置后的字体应用到按钮上
        self.toolButton.setText(_translate("Form", "帮助"))

        self.SubtitleLabel_3.setText(_translate("Form", "正在获取分析结果"))
        # 在原来的代码中添加设置字体大小的部分
        font2 = QFont()
        font2.setPointSize(17)  # 设置字体大小为16
        font2.setFamily("黑体")  # 设置字体为宋体
        self.toolButton_5.setFont(font2)  # 将设置后的字体应用到按钮上
        self.toolButton_5.setText(_translate("Form", "添加影像"))
        # 在原来的代码中添加设置字体大小的部分
        # font3 = QFont()
        # font3.setPointSize(16)  # 设置字体大小为16
        # font3.setFamily("黑体")  # 设置字体为宋体
        # self.BodyLabel_9.setFont(font3)  # 将设置后的字体应用到按钮上
        self.BodyLabel_9.setText(_translate("Form", "预测分析结果"))
        # 在原来的代码中添加设置字体大小的部分
        # font = QFont()
        # font.setPointSize(16)  # 设置字体大小为16
        # font.setFamily("黑体")  # 设置字体为宋体
        # self.PrimaryPushButton.setFont(font)  # 将设置后的字体应用到按钮上
        self.PrimaryPushButton.setText(_translate("Form", "生成报告"))


    def getPredictData(self):
        time.sleep(2)

        class_values = random.randint(1, 4)

        probability_values = random.uniform(0.5, 1)
        preclass_values = random.uniform(probability_values, 1)
        self.text_edit.setText(
            f"糖网分级共为五级，Class: {class_values}, 您的分级概率为，Probability: {probability_values}, 您的最大概率为，Prediction: {preclass_values} \n您平时需要特别注意以下几点，并且按照医生的建议进行治疗和药物管理：1.控制血糖平衡 2.定期眼科检查 3.戒烟限酒，减少并发症的风险。 \n建议您服用的药物有：1.口服类降糖药，如二甲双胍、磺脲类药物等，用于帮助控制血糖水平 2.抗高血压药物，如ACE抑制剂、ARBs等，用于控制高血压 \n注：具体用药规则请谨遵医嘱。")
        style_sheet = "QTextEdit { color: black; font-size: 20px; font-family: Arial; }"
        self.text_edit.setStyleSheet(style_sheet)


from qfluentwidgets import BodyLabel, IndeterminateProgressBar, PrimaryPushButton, SimpleCardWidget, SubtitleLabel

# if __name__ == "__main__":
#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()

#     ui.setupUi(Form)
#     # #1
#     # Form.show()
#     # 2
#     # 设置界面最大化
#     Form.showMaximized()

#     # 设置底部间距为100像素
#     screen_rect = app.primaryScreen().geometry()
#     form_rect = Form.geometry()
#     Form.setMaximumHeight(screen_rect.height() - 60)

    # # 限制窗体的宽度
    # Form.resize(screen_rect.width() - 50, Form.height())

    # # 限制窗体的左右宽度
    # left_margin = 50  # 左侧间距
    # right_margin = 50  # 右侧间距
    # Form.setGeometry(left_margin, Form.geometry().top(), screen_rect.width() - left_margin - right_margin,
    #                  Form.geometry().height())

    # # 设置右侧间距为50像素
    # screen_rect = app.primaryScreen().geometry()
    # form_rect = Form.geometry()
    # Form.setGeometry(form_rect.x(), form_rect.y(), screen_rect.width() - 50, form_rect.height())

    # 设置左侧间距为50像素
    # Form.setGeometry(50, Form.geometry().top(), Form.geometry().width(), Form.geometry().height())

    # # 设置左侧间距为50像素
    # screen_rect = app.primaryScreen().geometry()
    # form_rect = Form.geometry()
    # Form.setGeometry(60, form_rect.y(), screen_rect.width() - 60, form_rect.height())

    # sys.exit(app.exec_())

#
# app = QtWidgets.QApplication(sys.argv)
# Form = QtWidgets.QWidget()
# ui = Ui_Form()
#
# ui.setupUi(Form)
#
# # 设置界面最大化
# Form.showMaximized()
#
# # 设置底部间距为100像素
# screen_rect = app.primaryScreen().geometry()
# form_rect = Form.geometry()
# Form.setMaximumHeight(screen_rect.height() - 100)
#
# sys.exit(app.exec_())
