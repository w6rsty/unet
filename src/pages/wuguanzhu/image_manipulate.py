from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QColor, QPen, QBrush, QPainter
from PyQt5.QtCore import Qt
from skimage import io
import numpy as np
from PIL import Image
from enum import Enum
import cv2

import src.config as cfg

class OperationMode(Enum):
    NONE = -1           # 无操作
    GLOBAL_RECOGNIZE = 0    # 大图识别
    ADD_RECT = 1        # 矩形增加
    DELETE_RECT = 2     # 矩形删除
    MANUAL_ADD = 3     # 手动添加
    MANUAL_DELETE = 4   # 手动删除
    REGION_GROW = 5     # 区域生长
    RETINA_SEG = 6      # 眼底分区
    RETINA_SEG_1 = 7      # 眼底分区
    RECT_RATIO = 8      # 矩形占比

def np2pixmap(np_img):
    height, width, channel = np_img.shape
    bytesPerLine = 3 * width
    qImg = QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (255, 255, 255),
    (192, 192, 192),
    (64, 64, 64),
    (0, 0, 127),
    (192, 0, 192),
]

class ImageManipulatePanel(QWidget):
    def __init__(self, jsonLibrary, model, mode, parent=None):
        super().__init__(parent)

        self.jsonlibrary = jsonLibrary
        self.model = model

        self.mode = mode

        self.circle1 = None
        self.click_point = None
        self.radius = None
        self.end_pos = None
        self.circle = None

        # configs
        self.last_click_pos = None
        self.half_point_size = 5
        self.line_width = 3
        # app stats
        self.image_path = None
        self.color_idx = 0
        self.bg_img = None
        self.is_mouse_down = False
        self.rect = None
        self.point_size = self.half_point_size * 2
        self.start_point = None
        self.end_point = None
        self.start_pos = (None, None)
        self.mask_c = np.zeros((1024, 1024, 3), dtype="uint8")
        self.coordinate_history = []
        self.history = []  # 历史记录
        self.restore_region_history = {}  # 恢复区域的历史记录
        self.initial_image = None  # 记录最初图片的样子
        self.view1 = QGraphicsView()
        self.view2 = QGraphicsView()

        self.pen = QPen(QColor(255, 0, 0))
        self.pen.setWidth(2)

        self.color_idx = 0 

        self.half_point_size = 2
        self.point_size = 2 * self.half_point_size
        #################################################################
        # 分隔
        self.splitter = QSplitter(Qt.Horizontal)

        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)

        # 确保在初始化方法中设置了正确的滚动区域，以便可以滚动查看整个图像
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.splitter)
        
        self.splitter.addWidget(self.view1)
        self.splitter.addWidget(self.view2)

        self.setLayout(layout)

    def setImageByPath(self, path):
        img_np = io.imread(path)
        if len(img_np.shape) == 2:
            img_3c = np.repeat(img_np[:, :, None], 3, axis=-1)
        else:
            img_3c = img_np

        max_width = 99999
        max_height = 99999
        if img_3c.shape[0] > max_height or img_3c.shape[1] > max_width:
            img_3c = self.resize_image(img_3c, max_width, max_height)

        self.img_3c = img_3c
        self.image_path = path
        self.initial_image = np.copy(self.img_3c)
        pixmap = np2pixmap(self.img_3c)

        H, W, _ = self.img_3c.shape
        H, W, _ = self.img_3c.shape

        if hasattr(self, "scene"):
            self.view.setScene(None)
            del self.scene
        if hasattr(self, "scene2"):
            self.view.setScene(None)
            del self.scene2

        self.scene = QGraphicsScene(0, 0, W, H)
        self.scene2 = QGraphicsScene(0, 0, W, H)
        self.end_point = None
        self.rect = None
        self.bg_img1 = self.scene.addPixmap(pixmap)
        self.bg_img2 = self.scene2.addPixmap(pixmap)
        self.bg_img1.setPos(0, 0)
        self.bg_img2.setPos(0, 0)
        self.view1.setScene(self.scene)  # 在第一个视图中显示图像
        self.view2.setScene(self.scene2)  # 在第二个视图中显示相同的图像-

        # # 0: 未选中, 1: 左侧选中, 2: 右侧选中
        self.hoveredView = 0
        self.view1.enterEvent = self.enterLeft
        self.view1.leaveEvent = self.leaveLeft
        self.scene.mousePressEvent = self.mouse_press
        self.scene.mouseMoveEvent = self.mouse_move
        self.scene.mouseReleaseEvent = self.mouse_release

        self.view2.enterEvent = self.enterRight
        self.view2.leaveEvent = self.leaveLeft

    def setImage(self, id):
        path = self.jsonlibrary.getJsonById(id)['imgPath']
        self.setImageByPath(path)

    def update(self):
        # 找到两个数组中不同的像素点
        different_pixels = np.any(self.img_3c != self.initial_image, axis=-1)

        # 创建一个红色半透明的图像
        height, width = different_pixels.shape
        result_image = np.zeros((height, width, 4), dtype=np.uint8)
        result_image[different_pixels] = [128, 0, 0, 50]
        # 打开RGB图像和RGBA图像
        rgb_image = Image.fromarray(np.uint8(self.initial_image))
        rgba_image = Image.fromarray(np.uint8(result_image))

        # 将RGBA图像叠加到RGB图像上
        result_image = Image.alpha_composite(rgb_image.convert("RGBA"), rgba_image).convert("RGB")
        # 将图像转换为NumPy数组
        image_array = np.array(result_image)
        self.img_3c = image_array


    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            # 如果按住 Ctrl 键，则执行缩放事件
            delta = event.angleDelta().y() / 120
            factor = 1.1 if delta > 0 else 0.9
            if self.hoveredView == 1:
                self.view.scale(factor, factor)
            elif self.hoveredView == 2:
                self.view2.scale(factor, factor)
        else:
            # 如果没有按住 Shift 键，则执行默认的滚轮事件
            super().wheelEvent(event)

    def enterLeft(self, event):
        self.hoveredView = 1

    def enterRight(self, event):
        self.hoveredView = 2

    def leaveLeft(self, event):
        self.hoveredView = 0
    
    def mouse_press(self, ev):
        x, y = ev.scenePos().x(), ev.scenePos().y()

        try:
            if self.mode == OperationMode.ADD_RECT: # 矩形增加
                # 处理绘制逻辑
                self.is_mouse_down = True
                self.start_pos = ev.scenePos().x(), ev.scenePos().y()
                self.start_point = self.scene.addEllipse(
                    x - self.half_point_size,
                    y - self.half_point_size,
                    self.point_size,
                    self.point_size,
                    pen=QPen(QColor("red")),
                    brush=QBrush(QColor("red")),
                )
                self.coordinate_history.append((x, y))
                self.history.append(np.copy(self.img_3c))
                self.last_click_pos = (x, y)
            elif self.mode == OperationMode.RECT_RATIO: # 矩形占比
                # 处理差异模式逻辑
                self.is_mouse_down = True
                self.start_pos = ev.scenePos().x(), ev.scenePos().y()
                self.start_point = self.scene.addEllipse(
                    x - self.half_point_size,
                    y - self.half_point_size,
                    self.point_size,
                    self.point_size,
                    pen=QPen(QColor("yellow")),
                    brush=QBrush(QColor("yellow")),
                )
                self.coordinate_history.append((x, y))
                self.history.append(np.copy(self.img_3c))
            elif self.mode ==OperationMode.DELETE_RECT: # 矩形删除
                # 处理恢复模式逻辑
                self.is_mouse_down = True
                self.start_pos = ev.scenePos().x(), ev.scenePos().y()
                self.start_point = self.scene.addEllipse(
                    x - self.half_point_size,
                    y - self.half_point_size,
                    self.point_size,
                    self.point_size,
                    pen=QPen(QColor("green")),
                    brush=QBrush(QColor("green")),
                )
                self.restore_state = np.copy(self.img_3c)
            elif self.mode == OperationMode.MANUAL_ADD: # 手动添加
                self.is_mouse_down = True
                self.drawing = True
                self.points = [ev.scenePos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
            elif self.mode == OperationMode.MANUAL_DELETE: # 手动删除   
                self.is_mouse_down = True
                self.deleteing = True
                self.points = [ev.scenePos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
            elif self.mode == OperationMode.REGION_GROW: # 区域生长
                self.is_mouse_down = True
                self.history.append(np.copy(self.img_3c))
                self.flooding = True
                self.pa = ev.scenePos()

            elif self.mode == OperationMode.RETINA_SEG: # 眼底分区
                self.is_mouse_down = True
                self.start_pos = ev.scenePos()
                self.click_point = QGraphicsEllipseItem(
                    self.start_pos.x() - 2,  # 调整圆心坐标以使其居中
                    self.start_pos.y() - 2,
                    4,  # 设置圆的直径
                    4,
                )
                self.click_point.setPen(QPen(QColor("yellow")))
                self.click_point.setBrush(QBrush(QColor("yellow")))
                self.scene.addItem(self.click_point)

            elif self.mode == OperationMode.RETINA_SEG_1:
                self.end_pos = ev.scenePos()  # 记录第二个点击的点
                self.radius = ((self.end_pos.x() - self.start_pos.x()) ** 2 + (
                        self.end_pos.y() - self.start_pos.y()) ** 2) ** 0.5  # 计算圆的半径

        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def mouse_move(self, ev):
        try:
            if not self.is_mouse_down:
                return
            if self.mode != OperationMode.MANUAL_ADD and self.mode !=  OperationMode.MANUAL_DELETE:
                x, y = ev.scenePos().x(), ev.scenePos().y()

                if self.rect is not None:
                    self.scene.removeItem(self.rect)
                sx, sy = self.start_pos
                xmin = int(min(x, sx))
                xmax = int(max(x, sx))
                ymin = int(min(y, sy))
                ymax = int(max(y, sy))

                if self.mode == OperationMode.ADD_RECT: # 矩形增加
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("red"))
                    )
                if self.mode == OperationMode.RECT_RATIO: # 矩形占比
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("yellow"))
                    )
                elif self.mode == OperationMode.DELETE_RECT: # 矩形删除
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("green"))
                    )
            else:
                if self.mode == OperationMode.MANUAL_ADD and self.drawing:

                    current_point = ev.scenePos()
                    if len(self.points) > 0:
                        # 使用QPainter进行绘制
                        if self.tag == 0:
                            self.pixmap = np2pixmap(self.img_3c)

                            self.tag = 1
                        painter = QPainter(self.pixmap)

                        painter.setPen(self.pen)
                        painter.drawLine(self.points[-1], current_point)
                        painter.end()
                        if self.bg_img is not None:
                            self.scene.removeItem(self.bg_img)
                        self.bg_img = self.scene.addPixmap(self.pixmap)

                        self.points.append(current_point)

                elif self.mode ==  OperationMode.MANUAL_DELETE and self.deleteing:

                    current_point = ev.scenePos()
                    if len(self.points) > 0:
                        # 使用QPainter进行绘制
                        if self.tag == 0:
                            self.pixmap = np2pixmap(self.img_3c)
                            self.tag = 1
                        painter = QPainter(self.pixmap)
                        painter.setPen(self.pen)
                        painter.drawLine(self.points[-1], current_point)
                        painter.end()
                        if self.bg_img is not None:
                            self.scene.removeItem(self.bg_img)
                        self.bg_img = self.scene.addPixmap(self.pixmap)

                        self.points.append(current_point)
        except Exception as e:
            pass

    def update_image(self):
        self.update()
        try:

            pixmap = np2pixmap(self.img_3c)
            self.bg_img = self.scene.addPixmap(pixmap)
            self.bg_img.setPos(0, 0)
        except Exception as e:
            pass

    def mouse_release(self, ev):
        self.is_mouse_down = False

        if self.mode == OperationMode.RECT_RATIO: # 矩形占比
            xmin = int(min(self.start_pos[0], ev.scenePos().x()))
            xmax = int(max(self.start_pos[0], ev.scenePos().x()))
            ymin = int(min(self.start_pos[1], ev.scenePos().y()))
            ymax = int(max(self.start_pos[1], ev.scenePos().y()))
            self.show_difference_percentage(xmin, xmax, ymin, ymax)


        elif self.mode == OperationMode.DELETE_RECT: # 矩形删除
            xmin = int(min(self.start_pos[0], ev.scenePos().x()))
            xmax = int(max(self.start_pos[0], ev.scenePos().x()))
            ymin = int(min(self.start_pos[1], ev.scenePos().y()))
            ymax = int(max(self.start_pos[1], ev.scenePos().y()))

            region_to_restore = self.initial_image[ymin:ymax, xmin:xmax]

            self.img_3c[ymin:ymax, xmin:xmax] = region_to_restore
            self.update_image()

        elif self.mode == OperationMode.MANUAL_ADD and self.drawing:
            try:
                self.drawing = False
                self.tag = 0
                if len(self.points) >= 3:
                    start_point = self.points[0]
                    end_point = self.points[-1]

                self.drawEdge(start_point, end_point)
                self.fillMask()
                self.applyMask()
                # self.update_image()
            except Exception as e:
                print(e)
        elif self.mode == OperationMode.MANUAL_DELETE and self.deleteing:
            try:
                self.deleteing = False
                self.tag = 0
                # print(self.points)
                if len(self.points) >= 3:
                    start_point = self.points[0]
                    end_point = self.points[-1]

                self.drawEdge(start_point, end_point)

                self.deleteMask()
            except Exception as e:
                print(e)
        elif self.mode == OperationMode.ADD_RECT: # 矩形增加
            color = colors[self.color_idx]
            self.mask_c[int(min(self.start_pos[1], ev.scenePos().y())):int(max(self.start_pos[1], ev.scenePos().y())),
            int(min(self.start_pos[0], ev.scenePos().x())):int(max(self.start_pos[0], ev.scenePos().x()))] = color
            self.color_idx = (self.color_idx + 1) % len(colors)

            # time.sleep(1)

            xmin = int(min(self.start_pos[0], ev.scenePos().x()))
            xmax = int(max(self.start_pos[0], ev.scenePos().x()))
            ymin = int(min(self.start_pos[1], ev.scenePos().y()))
            ymax = int(max(self.start_pos[1], ev.scenePos().y()))

            region_to_render_white = self.initial_image[ymin:ymax, xmin:xmax]
            if region_to_render_white.shape[0] > 0 and region_to_render_white.shape[1] > 0:
                print(region_to_render_white.shape)
                image = Image.fromarray(region_to_render_white)
                segmented_image = self.model.getSmallModel().detect_image(image)
                image_array = np.array(segmented_image)
                self.img_3c[ymin:ymax, xmin:xmax] = image_array

            elif region_to_render_white.shape[0] < 1 and region_to_render_white.shape[1] < 1:
                return
            self.update_image()
        elif self.mode == OperationMode.REGION_GROW and self.flooding:
                self.flooding = False
                x = int(self.pa.x())
                y = int(self.pa.y())

                img = np.copy(self.img_3c)

                w, h = img.shape[0:2]
                # # 注意mask遮罩层为0 类型为一个uint8 比原始图像长宽都多2
                mask = np.zeros([w + 2, h + 2], dtype=np.uint8)

                cv2.floodFill(img, mask, (x, y), (255, 0, 0), (10, 10, 10), (10, 10, 10),
                              flags=cv2.FLOODFILL_FIXED_RANGE)
                # cv2.imwrite('high_contrast_color_image.jpg', img)
                self.img_3c = img
                self.update_image()
                # self.show_difference_percentage()
        elif self.mode == OperationMode.RETINA_SEG:
            self.mode = OperationMode.RETINA_SEG_1
        elif self.mode == OperationMode.RETINA_SEG_1:
            self.mode = OperationMode.RETINA_SEG

            radius = ((self.end_pos.x() - self.start_pos.x()) ** 2 + (
                    self.end_pos.y() - self.start_pos.y()) ** 2) ** 0.5  # 计算圆的半径

            # 创建圆形图形项
            x, y = self.start_pos.x(), self.start_pos.y()
            self.circle = QGraphicsEllipseItem(
                x - radius,
                y - radius,
                radius * 2,
                radius * 2
            )
            self.circle.setPen(QPen(QColor("black")))
            self.scene.addItem(self.circle)
            self.circle1 = QGraphicsEllipseItem(
                x - 13.33*radius,
                y - 13.33*radius,
                radius * 26.66,
                radius * 26.66
            )
            self.circle1.setPen(QPen(QColor("yellow")))
            self.scene.addItem(self.circle1)
            self.circle2 = QGraphicsEllipseItem(
                x - 20*radius,
                y - 20*radius,
                radius * 40,
                radius * 40
            )
            self.circle2.setPen(QPen(QColor("green")))
            self.scene.addItem(self.circle2)
            circle_rect = self.circle.boundingRect()
            xmin, ymin, xmax, ymax = int(circle_rect.left()), int(circle_rect.top()), int(circle_rect.right()), int(
                circle_rect.bottom())
            region_to_compare = self.initial_image[ymin:ymax, xmin:xmax]
            region_to_render = self.img_3c[ymin:ymax, xmin:xmax]

            diff_percentage = 1 - ((region_to_compare == region_to_render).sum() / region_to_compare.size)
            circle_rect1 = self.circle1.boundingRect()
            xmin, ymin, xmax, ymax = int(circle_rect1.left()), int(circle_rect1.top()), int(circle_rect1.right()), int(
                circle_rect1.bottom())
            region_to_compare = self.initial_image[ymin:ymax, xmin:xmax]
            region_to_render = self.img_3c[ymin:ymax, xmin:xmax]

            diff_percentage1 = 1 - ((region_to_compare == region_to_render).sum() / region_to_compare.size)
            circle_rect2 = self.circle2.boundingRect()
            xmin, ymin, xmax, ymax = int(circle_rect2.left()), int(circle_rect2.top()), int(circle_rect2.right()), int(
                circle_rect2.bottom())
            region_to_compare = self.initial_image[ymin:ymax, xmin:xmax]
            region_to_render = self.img_3c[ymin:ymax, xmin:xmax]

            diff_percentage2 = 1 - ((region_to_compare == region_to_render).sum() / region_to_compare.size)

            # 创建弹窗来显示百分比和区域
            region_info = f"Region:\n{region_to_render}"
            message = f" black无灌注区域占圆形区域 : {diff_percentage:.2%}\n\n"
            message1 = f" yellow无灌注区域占圆形区域 : {diff_percentage1:.2%}\n\n"
            message2 = f"green无灌注区域占圆形区域 : {diff_percentage2:.2%}\n\n"

            msgBox = QMessageBox()
            msgBox.setWindowTitle("Difference Percentage")

            msgBox.setText(message + message1 + message2)

            okButton = msgBox.addButton(QMessageBox.Ok)
            okButton.setText("OK")

            msgBox.exec_()

    def show_message_box(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("识别中...")
        message_box.setWindowTitle("信息消息框")
        message_box.show()


    ###########################################
    # 按钮函数
    ###########################################
    # 不设置模式的函数，先将模式设置为NONE

    # 加载图片
    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, '选择图片', './', 'Images(*.png *.jpg *.jpeg *.bmp *.gif)')[0]
        if not path:
            print('未指定图像路径，请选择一个图像')
            return
        
        self.setImageByPath(path)


    # 读取历史
    def readHistory(self):
        self.loadImage()

    # 大图识别(识别整个图片， 使用log4)
    def globalRecognize(self):
        self.mode = OperationMode.NONE
        print("大图识别")
        self.global_recognize()
    
    # 矩形增加(添加矩形识别区域)
    def addRect(self):
        print("当前模式: 矩形增加")
        self.mode = OperationMode.ADD_RECT

    # 矩形删除(删除矩形识别区域)
    def deleteRect(self):
        print("当前模式: 矩形删除")
        self.mode = OperationMode.DELETE_RECT

    # 手动添加(手动添加标注区域)
    def manualAdd(self):
        print("当前模式: 手动添加")
        self.mode = OperationMode.MANUAL_ADD

    # 手动删除(手动删除标注区域)
    def manualDelete(self):
        print("当前模式: 手动删除")
        self.mode = OperationMode.MANUAL_DELETE

    # 区域生长
    def regionGrow(self):
        print("当前模式: 区域生长")
        self.mode = OperationMode.REGION_GROW

    # 眼底分区
    def retinaSeg(self):
        print("当前模式: 眼底分区")
        self.mode = OperationMode.RETINA_SEG

    # 矩形占比(
    def rectRatio(self):
        print("当前模式: 矩形占比")
        self.mode = OperationMode.RECT_RATIO

    # 撤销操作(撤销上一步操作)
    def undo(self):
        if self.history:
            self.img_3c = self.history.pop()
            self.update_image()
        else:
            print("无法撤销")

    # 数据保存
    def saveData(self):
        if hasattr(self, "initial_image"):
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果图像", ".", "PNG Files (*.png)"
            )

            if file_path:
                result_image = Image.fromarray(self.img_3c.astype('uint8'))
                result_image.save(file_path)

    # 掩膜保存
    def saveMask(self):
        if hasattr(self, "initial_image"):
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果图像", ".", "PNG Files (*.png)"
            )

            if file_path:
                # 找到颜色不同的像素点
                different_pixels = np.all(self.initial_image != self.img_3c, axis=-1)

                # 创建一个全黑图像，与输入RGB图像相同大小
                height, width, _ = self.img_3c.shape
                output_image = np.zeros((height, width), dtype=np.uint8)
                # 在不同的像素点上绘制白色
                output_image[different_pixels] = 255
                # 保存二值灰度图像
                result_image = Image.fromarray(output_image.astype('uint8'))
                result_image.save(file_path)

    def drawEdge(self, point1, point2):
        if len(self.points) >= 2:
            for i in range(len(self.points) - 1):
                self.scene.addLine(point1.x(), point1.y(), point2.x(), point2.y(), self.pen)

    def fillMask(self):
        if self.img_3c is not None:
            height, width, _ = self.img_3c.shape
            self.mask = np.zeros((height, width, 4), dtype=np.uint8)  # 4通道图像

            points_array = np.array(
                [(point.x(), point.y()) for point in self.points], dtype=np.int32
            )

            cv2.fillPoly(self.mask, [points_array], (128, 0, 0, 50))

    def deleteMask(self):
        if self.img_3c is not None:
            height, width, _ = self.img_3c.shape
            points_array = np.array(
                [(point.x(), point.y()) for point in self.points], dtype=np.int32
            )

            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.fillPoly(mask, [points_array], 1)

            # 3. 使用遮罩提取多边形区域
            extracted_region = cv2.bitwise_and(self.initial_image, self.initial_image, mask=mask)

            # 4. 将提取的区域替换为要填充的内容
            result_image = self.img_3c.copy()  # 创建目标图像的副本
            result_image[mask == 1] = extracted_region[mask == 1]

            self.img_3c = result_image
            self.update_image()

    def applyMask(self):
        if self.img_3c is not None and self.mask is not None:
            mask_inv = cv2.bitwise_not(self.mask[:, :, 3])
            img_bg = cv2.bitwise_and(self.img_3c, self.img_3c, mask=mask_inv)

            img_fg = self.mask[:, :, :3]

            result = cv2.add(img_bg, img_fg)
            self.img_3c = result
            self.update_image()
            
    def resize_image(self, img, max_width, max_height):
        img_height, img_width, _ = img.shape
        if img_width > max_width or img_height > max_height:
            scale_x = max_width / img_width
            scale_y = max_height / img_height
            scale = min(scale_x, scale_y)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img = Image.fromarray(img)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img = np.array(img)

        return img
    
    def global_recognize(self):
        color = colors[self.color_idx]
        image_size = self.img_3c.shape
        height, width = image_size[:2]
        # 识别整个图像
        self.mask_c[0:height, 0:width] = color
        self.color_idx = (self.color_idx + 1) % len(colors)

        region_to_render_white = self.initial_image[0:height, 0:width]
        if region_to_render_white.shape[0] > 0 and region_to_render_white.shape[1] > 0:
            print(region_to_render_white.shape)
            image = Image.fromarray(region_to_render_white)
            segmented_image = self.model.getLargeModel().detect_image(image)
            image_array = np.array(segmented_image)
            self.img_3c[0:height, 0:width] = image_array

        elif region_to_render_white.shape[0] < 1 and region_to_render_white.shape[1] < 1:
            return
        self.update_image()