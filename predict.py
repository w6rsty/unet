import hashlib
import sys
import threading
import wmi

import cv2
from PyQt5 import Qt, QtWidgets
from PyQt5.QtGui import QIcon, QBrush, QPainter, QPen, QPixmap, QColor, QImage, QGuiApplication
from PyQt5.QtWidgets import (
    QFileDialog,
    QApplication,
    QGraphicsEllipseItem,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QShortcut,
    QMessageBox,
    QGraphicsScene,
    QGraphicsView,
    QLabel, QDesktopWidget, QAction, QSpacerItem, QSizePolicy, QSlider, QDialog, QLineEdit,
)
import numpy as np
from skimage import io
import time
from PIL import Image
from unet import Unet
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QSplitter

from qfluentwidgets import *

# 创建Unet实例，替换为您的模型路径和参数
model_path = 'logs3/best_epoch_weights.pth'
num_classes = 2
unet_instance = Unet(model_path=model_path, num_classes=num_classes, input_shape=[256, 256], cuda=False)

# 创建Unet实例，替换为您的模型路径和参数
model_path = 'logs4/best_epoch_weights.pth'
num_classes = 2
unet_instance1 = Unet(model_path=model_path, num_classes=num_classes, input_shape=[1024, 1024], cuda=False)


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


class MaterialButton(QPushButton):
    def __init__(self, text, parent=None):
        super(MaterialButton, self).__init__(text, parent)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #A9A9A9; /* Material Design Blue 500 */
                color: white;
                border-radius: 20px; /* Increase border radius for larger buttons */
                padding: 15px 20px; /* Increase padding for larger buttons */
                font-size: 20px; /* Increase font size for larger buttons */

            }
            QPushButton:hover {
                background-color: #808080; /* Material Design Blue 700 */
            }
            """
        )


class Window(QWidget):

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            zoom_factor = 1.15  # 缩放因子，你可以根据需要调整
            if event.angleDelta().y() > 0:
                # 向上滚动鼠标滚轮，放大图片
                self.view1.scale(zoom_factor, zoom_factor)
            else:
                # 向下滚动鼠标滚轮，缩小图片
                self.view1.scale(1 / zoom_factor, 1 / zoom_factor)
        else:
            # 如果没有按住 Shift 键，则执行默认的滚轮事件
            super().wheelEvent(event)
        if event.modifiers() & Qt.ControlModifier:
            zoom_factor = 1.15  # 缩放因子，你可以根据需要调整
            if event.angleDelta().y() > 0:
                # 向上滚动鼠标滚轮，放大图片
                self.view2.scale(zoom_factor, zoom_factor)
            else:
                # 向下滚动鼠标滚轮，缩小图片
                self.view2.scale(1 / zoom_factor, 1 / zoom_factor)
        else:
            # 如果没有按住 Shift 键，则执行默认的滚轮事件
            super().wheelEvent(event)

    def __init__(self):
        super().__init__()
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
        self.mode = "draw"  # 当前模式，默认为绘制模式
        self.restore_region_history = {}  # 恢复区域的历史记录
        self.initial_image = None  # 记录最初图片的样子
        self.view1 = QGraphicsView()
        self.view2 = QGraphicsView()

        # 创建QSplitter以容纳两个视图
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.view1)
        splitter.addWidget(self.view2)
        splitter.addWidget(self.view1)
        splitter.addWidget(self.view2)
        self.setCentralWidget(splitter)  # 设置QSplitter为主窗口的中央组件

        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)

        # 确保在初始化方法中设置了正确的滚动区域，以便可以滚动查看整个图像
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        pixmap = QPixmap(1024, 1024)

        # vbox = QVBoxLayout(self)
        # vbox.addWidget(self.view)
        pixmap = QPixmap(1024, 1024)

        # vbox = QVBoxLayout(self)
        # vbox.addWidget(self.view)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(3)

        self.pen = QPen(QColor(0, 255, 0))
        self.pen.setWidth(self.slider.value())

        load_button = MaterialButton("加载图片")
        save_button = MaterialButton("数据保存")
        undo_button = MaterialButton("撤销操作")
        draw_button = MaterialButton("大图识别")
        add_button = MaterialButton("矩形增加")
        restore_button = MaterialButton("矩形删除")
        difference_button = MaterialButton("矩形占比")
        diff_button = MaterialButton("眼底分区")
        edge_button = MaterialButton("手动添加")
        delete_button = MaterialButton("手动删除")
        flood_button = MaterialButton("区域生长")
        sss_button = MaterialButton("读取历史")
        save2_button = MaterialButton("掩模保存")
        load_button = MaterialButton("加载图片")
        save_button = MaterialButton("数据保存")
        undo_button = MaterialButton("撤销操作")
        draw_button = MaterialButton("大图识别")
        add_button = MaterialButton("矩形增加")
        restore_button = MaterialButton("矩形删除")
        difference_button = MaterialButton("矩形占比")
        diff_button = MaterialButton("眼底分区")
        edge_button = MaterialButton("手动添加")
        delete_button = MaterialButton("手动删除")
        flood_button = MaterialButton("区域生长")
        sss_button = MaterialButton("读取历史")
        save2_button = MaterialButton("掩模保存")

        button_style = (
            "background-color: #A9A9A9; color: white;"
            "border-radius: 8px; padding: 12px 18px; font-size: 10px;"
        )

        # 设置初始窗口状态为普通大小窗口，而不是全屏
        # 获取屏幕的大小和任务栏高度
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry(desktop.primaryScreen())
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        taskbar_height = desktop.availableGeometry().height() - screen_geometry.height()

        # 设置窗口初始位置和大小，以避免覆盖任务栏
        self.setGeometry(0, 0, screen_width, screen_height - taskbar_height - 112)

        hbox = QHBoxLayout(self)
        # 设置按钮之间的间距
        hbox.setSpacing(10)  # 设置按钮之间的间距为20像素
        hbox.addWidget(load_button)
        hbox.addWidget(save_button)

        hbox.addWidget(undo_button)
        hbox.addWidget(draw_button)
        hbox.addWidget(restore_button)
        hbox.addWidget(difference_button)
        hbox.addWidget(diff_button)
        hbox.addWidget(edge_button)
        hbox.addWidget(delete_button)
        hbox.addWidget(flood_button)
        hbox.addWidget(add_button)
        hbox.addWidget(sss_button)
        hbox.addWidget(save2_button)
        hbox.addWidget(self.slider)

        self.quit_shortcut = QShortcut("Esc", self)
        self.quit_shortcut.activated.connect(self.quit)
        # load_button.setStyleSheet("margin-right: 10px;")  # 添加右侧边距
        # save_button.setStyleSheet("margin-left: 20px;")  # 添加左侧边距
        load_button.clicked.connect(self.load_image)
        save_button.clicked.connect(self.save_mask)
        undo_button.clicked.connect(self.undo_last_edit)
        draw_button.clicked.connect(self.draw_mode)
        restore_button.clicked.connect(self.restore_mode)
        difference_button.clicked.connect(self.difference_mode)
        diff_button.clicked.connect(self.diff_mode)
        edge_button.clicked.connect(self.toggle_edge_mode)
        delete_button.clicked.connect(self.delete_edge)
        add_button.clicked.connect(self.add_mode)
        flood_button.clicked.connect(self.flood)
        sss_button.clicked.connect(self.sss_img)
        save2_button.clicked.connect(self.save_mask2)
        self.slider.valueChanged.connect(self.updatePenWidth)

        toolbar = self.addToolBar("Tools")



        # 添加按钮
        toolbar.addWidget(load_button)
        # 创建一个透明的小部件来模拟不可见的间隔
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget)

        toolbar.addWidget(sss_button)
        spacer_widget2 = QWidget()
        spacer_widget2.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget2.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget2)
        toolbar.addWidget(draw_button)
        spacer_widget5 = QWidget()
        spacer_widget5.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget5.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget5)
        toolbar.addWidget(add_button)
        spacer_widget9 = QWidget()
        spacer_widget9.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget9.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget9)
        toolbar.addWidget(edge_button)
        spacer_widget1 = QWidget()
        spacer_widget1.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget1.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget1)
        toolbar.addWidget(restore_button)
        spacer_widget4 = QWidget()
        spacer_widget4.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget4.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget4)
        toolbar.addWidget(delete_button)
        spacer_widget8 = QWidget()
        spacer_widget8.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget8.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget8)
        toolbar.addWidget(flood_button)
        spacer_widget9 = QWidget()
        spacer_widget9.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget9.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget9)
        toolbar.addWidget(diff_button)
        spacer_widget6 = QWidget()
        spacer_widget6.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget6.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget6)
        toolbar.addWidget(difference_button)
        # 创建一个透明的小部件来模拟不可见的间隔
        spacer_widget12 = QWidget()
        spacer_widget12.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget12.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget12)
        toolbar.addWidget(undo_button)
        spacer_widget3 = QWidget()
        spacer_widget3.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget3.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget3)

        toolbar.addWidget(save_button)
        spacer_widget12 = QWidget()
        spacer_widget12.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget12.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget12)
        toolbar.addWidget(save2_button)
        spacer_widget12 = QWidget()
        spacer_widget12.setFixedWidth(10)  # 设置小部件宽度，这里设为10像素，你可以根据需要调整
        spacer_widget12.setStyleSheet("background: transparent;")  # 设置背景透明
        toolbar.addWidget(spacer_widget12)
        toolbar.addWidget(self.slider)

    def quit(self):
        QApplication.quit()

    def encrypt_mac_address(self,mac_address):
        sha256 = hashlib.sha256()
        sha256.update(mac_address.encode())
        encrypted_mac = sha256.hexdigest()
        encrypted_mac = encrypted_mac.replace("a","w")
        encrypted_mac = encrypted_mac.replace("b", "l")
        encrypted_mac = encrypted_mac.replace("c", "a")
        encrypted_mac = encrypted_mac.replace("d", "o")
        encrypted_mac = encrypted_mac.replace("e", "y")
        encrypted_mac = encrypted_mac.replace("f", "u")
        encrypted_mac = encrypted_mac.replace("g", "n")
        encrypted_mac = encrypted_mac.replace("h", "s")
        encrypted_mac = encrypted_mac.replace("i", "0417")
        encrypted_mac = encrypted_mac.replace("j", "0524")
        encrypted_mac = encrypted_mac.replace("k", "b")
        encrypted_mac = encrypted_mac.replace("l", "f")
        encrypted_mac = encrypted_mac.replace("m", "e")
        encrypted_mac = encrypted_mac.replace("n", "c")
        encrypted_mac = encrypted_mac.replace("w", "accde")
        encrypted_mac = encrypted_mac.replace("l", "bxcty")
        encrypted_mac = encrypted_mac.replace("1", "sdlkajhgfjkhsdfj")
        encrypted_mac = encrypted_mac.replace("2", "1l23e12qv")
        encrypted_mac = encrypted_mac.replace("3", "fjduslahf214451asdfslaij")
        return encrypted_mac

    def show_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("警告")

        layout = QVBoxLayout()

        label = QLabel("检测到未填写注册码或者注册码失效")
        layout.addWidget(label)

        input_text = QLineEdit()
        layout.addWidget(input_text)

        ok_button = QPushButton("确定")
        layout.addWidget(ok_button)

        dialog.setLayout(layout)

        def save_to_file():
            user_input = input_text.text()
            with open("cfg/cfg.txt", "w") as file:
                file.write(user_input + "\n")

            dialog.accept()

        ok_button.clicked.connect(save_to_file)

        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def load_image(self):
        # # 打开文件
        # cfg_path = "cfg/cfg.txt"  # 将文件路径替换为您要读取的文件
        # try:
        #     with open(cfg_path, 'r', encoding='utf-8') as file:
        #         # 读取文件内容
        #         file_contents = file.read().replace("\n","")
        #         c = wmi.WMI()
        #         bio = ""
        #         for bios_id in c.Win32_BIOS():
        #             # print(bios_id.SerialNumber.strip())
        #             bio += bios_id.SerialNumber.strip()
        #         code = bio
        #         mac_code = self.encrypt_mac_address(code)
        #         if file_contents!=mac_code:
        #             self.show_dialog()
        #             return


        # except FileNotFoundError:
        #     print(f"文件 '{cfg_path}' 未找到.")
        #     return
        # except Exception as e:
        #     print(f"发生错误: {str(e)}")
        #     return



        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", ".", "Image Files (*.png *.jpg *.bmp)"
        )

        if not file_path:
            print("未指定图像路径，请选择一个图像")
            return

        img_np = io.imread(file_path)
        if len(img_np.shape) == 2:
            img_3c = np.repeat(img_np[:, :, None], 3, axis=-1)
        else:
            img_3c = img_np

        max_width = 99999
        max_height = 99999
        if img_3c.shape[0] > max_height or img_3c.shape[1] > max_width:
            img_3c = self.resize_image(img_3c, max_width, max_height)

        self.img_3c = img_3c
        self.image_path = file_path
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
        self.view1.setScene(self.scene)  # 在第一个视图中显示图像
        self.view2.setScene(self.scene2)  # 在第二个视图中显示相同的图像-

        self.scene.mousePressEvent = self.mouse_press
        self.scene.mouseMoveEvent = self.mouse_move
        self.scene.mouseReleaseEvent = self.mouse_release



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

    def flood(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（区域生长模式）")  # 设置窗口标题
        self.mode = "flood"
        self.flooding = False

    def mouse_press(self, ev):
        x, y = ev.scenePos().x(), ev.scenePos().y()

        try:
            if self.mode == "draw":
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
            if self.mode == "add":
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
            elif self.mode == "difference":
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
            elif self.mode == "restore":
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
            elif self.mode == "describe":
                self.is_mouse_down = True
                self.drawing = True
                self.points = [ev.scenePos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
            elif self.mode == "delete":
                self.is_mouse_down = True
                self.deleteing = True
                self.points = [ev.scenePos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
            elif self.mode == "flood":
                self.is_mouse_down = True
                self.history.append(np.copy(self.img_3c))
                self.flooding = True
                self.pa = ev.scenePos()

            elif self.mode == "diff":
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

            elif self.mode == "diff1":
                self.end_pos = ev.scenePos()  # 记录第二个点击的点
                self.radius = ((self.end_pos.x() - self.start_pos.x()) ** 2 + (
                        self.end_pos.y() - self.start_pos.y()) ** 2) ** 0.5  # 计算圆的半径

        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def mouse_move(self, ev):
        try:
            if not self.is_mouse_down:
                return
            if self.mode != "describe" and self.mode != "delete":
                x, y = ev.scenePos().x(), ev.scenePos().y()

                if self.rect is not None:
                    self.scene.removeItem(self.rect)
                sx, sy = self.start_pos
                xmin = int(min(x, sx))
                xmax = int(max(x, sx))
                ymin = int(min(y, sy))
                ymax = int(max(y, sy))

                if self.mode == "draw":
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("red"))
                    )

                if self.mode == "add":
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("red"))
                    )
                if self.mode == "difference":
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("yellow"))
                    )
                elif self.mode == "restore":
                    self.rect = self.scene.addRect(
                        xmin, ymin, xmax - xmin, ymax - ymin, pen=QPen(QColor("green"))
                    )
            else:
                if self.mode == "describe" and self.drawing:

                    # try:
                    # print(self.points)

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

                        # self.bg_img.setPos(0, 0)


                # except Exception as e:
                #     print(e)

                elif self.mode == "delete" and self.deleteing:

                    # try:
                    # print(self.points)

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
            # self.scene.removeItem(self.bg_img)
            self.bg_img = self.scene.addPixmap(pixmap)
            # print(1111)
            self.bg_img.setPos(0, 0)
        except Exception as e:
            pass

    def mouse_release(self, ev):
        self.is_mouse_down = False
        if self.mode == "draw":
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
            # message_box = QMessageBox()
            # message_box.setIcon(QMessageBox.Information)
            # message_box.setText("正在识别")
            # message_box.setWindowTitle("信息消息框")
            # message_box.exec_()
            # timer = QTimer()
            # timer.timeout.connect(message_box.accept)
            if region_to_render_white.shape[0] > 600 and region_to_render_white.shape[1] > 600:
                print(region_to_render_white.shape)

                image = Image.fromarray(region_to_render_white)
                segmented_image = unet_instance1.detect_image(image)
                image_array = np.array(segmented_image)
                self.img_3c[ymin:ymax, xmin:xmax] = image_array
                # finally:\
                4
                #     message_thread.join()
            elif region_to_render_white.shape[0] < 1 and region_to_render_white.shape[1] < 1:
                return

            else:
                print(region_to_render_white.shape)
                image = Image.fromarray(region_to_render_white)
                segmented_image = unet_instance.detect_image(image)
                image_array = np.array(segmented_image)
                self.img_3c[ymin:ymax, xmin:xmax] = image_array
            self.update_image()
            # message_box = QMessageBox()
            # message_box.setIcon(QMessageBox.Information)
            # message_box.setText("识别完成")
            # message_box.setWindowTitle("信息消息框")
            # message_box.exec_()

        if self.mode == "difference":
            xmin = int(min(self.start_pos[0], ev.scenePos().x()))
            xmax = int(max(self.start_pos[0], ev.scenePos().x()))
            ymin = int(min(self.start_pos[1], ev.scenePos().y()))
            ymax = int(max(self.start_pos[1], ev.scenePos().y()))
            self.show_difference_percentage(xmin, xmax, ymin, ymax)


        elif self.mode == "restore":
            xmin = int(min(self.start_pos[0], ev.scenePos().x()))
            xmax = int(max(self.start_pos[0], ev.scenePos().x()))
            ymin = int(min(self.start_pos[1], ev.scenePos().y()))
            ymax = int(max(self.start_pos[1], ev.scenePos().y()))

            region_to_restore = self.initial_image[ymin:ymax, xmin:xmax]

            # time.sleep(1)

            self.img_3c[ymin:ymax, xmin:xmax] = region_to_restore
            self.update_image()

        elif self.mode == "describe" and self.drawing:
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
        elif self.mode == "delete" and self.deleteing:
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
        elif self.mode == "add":
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
                segmented_image = unet_instance.detect_image(image)
                image_array = np.array(segmented_image)
                self.img_3c[ymin:ymax, xmin:xmax] = image_array

            elif region_to_render_white.shape[0] < 1 and region_to_render_white.shape[1] < 1:
                return
            self.update_image()
        elif self.mode == "flood" and self.flooding:
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
        elif self.mode == "diff":
            self.mode = "diff1"
        elif self.mode == "diff1":
            self.mode = "diff"

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

            result = msgBox.exec_()

    def show_message_box(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("识别中...")
        message_box.setWindowTitle("信息消息框")
        message_box.show()

        # 设置一个定时器，延时2秒后自动关闭消息框
        timer = QTimer()
        timer.timeout.connect(message_box.accept)
        timer.start(1)  # 设置延时时间（以毫秒为单位)

    def undo_last_edit(self):
        if self.history:
            print(len(self.history))
            self.img_3c = self.history.pop()
            self.update_image()

    def view_history(self):
        if self.coordinate_history:
            coordinate_history_text = "\n".join([f"({x}, {y})" for x, y in self.coordinate_history])
            QMessageBox.information(self, "坐标历史记录", coordinate_history_text)
        else:
            QMessageBox.information(self, "坐标历史记录", "无可用历史记录.")

    def save_mask(self):
        if hasattr(self, "initial_image"):
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果图像", ".", "PNG Files (*.png)"
            )

            if file_path:
                result_image = Image.fromarray(self.img_3c.astype('uint8'))
                result_image.save(file_path)


    def save_mask2(self):
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
    def show_difference_percentage(self, xmin, xmax, ymin, ymax):
        region_to_compare = self.initial_image[ymin:ymax, xmin:xmax]
        region_to_render = self.img_3c[ymin:ymax, xmin:xmax]

        diff_percentage = 1 - ((region_to_compare == region_to_render).sum() / region_to_compare.size)

        # 创建弹窗来显示百分比和区域
        region_info = f"Region:\n{region_to_render}"
        message = f"无灌注区域占矩形区域 : {diff_percentage:.2%}"
        QMessageBox.information(self, "Difference Percentage", message)

    def toggle_mode(self):
        if self.mode == "draw":
            self.mode = "restore"
        else:
            self.mode = "draw"
            self.restore_region_history.clear()

    def toggle_edge_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（手绘添加模式）")  # 设置窗口标题
        self.mode = "describe"
        self.drawing = False
        self.points = []

    def delete_edge(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（手绘删除模式）")  # 设置窗口标题
        self.mode = "delete"
        self.deleteing = True
        self.points = []

    def fillMask(self):
        if self.img_3c is not None:
            height, width, _ = self.img_3c.shape
            self.mask = np.zeros((height, width, 4), dtype=np.uint8)  # 4通道图像

            points_array = np.array(
                [(point.x(), point.y()) for point in self.points], dtype=np.int32
            )
            # for point in self.points:
            #     print(self.img_3c[int(point.x()), int(point.y())])

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

    # 矩形删除
    def restore_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（矩形删除模式）")  # 设置窗口标题
        self.mode = "restore"

    # 矩形增加
    def draw_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（大模型识别模式）")  # 设置窗口标题
        self.mode = "draw"

    def difference_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（矩形占比模式）")  # 设置窗口标题
        self.mode = "difference"

    def drawEdge(self, point1, point2):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（手绘边缘模式）")  # 设置窗口标题
        if len(self.points) >= 2:
            for i in range(len(self.points) - 1):
                self.scene.addLine(point1.x(), point1.y(), point2.x(), point2.y(), self.pen)

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

    def add_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（小模型识别模式）")  # 设置窗口标题
        self.mode = "add"

    def updatePenWidth(self):
        # 更新笔刷的宽度
        width = self.slider.value()
        self.pen.setWidth(width)

    def diff_mode(self):
        self.setWindowTitle("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（视盘划分模式）")  # 设置窗口标题
        self.mode = "diff"

    # TODO: ok
    def sss_img(self):
        # 打开文件
        # cfg_path = "cfg/cfg.txt"  # 将文件路径替换为您要读取的文件
        # try:
        #     with open(cfg_path, 'r', encoding='utf-8') as file:
        #         # 读取文件内容
        #         file_contents = file.read().replace("\n", "")
                # import wmi
                # c = wmi.WMI()
                # bio = ""
                # for bios_id in c.Win32_BIOS():
                #     # print(bios_id.SerialNumber.strip())
                #     bio += bios_id.SerialNumber.strip()
                # code = bio
                # mac_code = self.encrypt_mac_address(code)

                # if file_contents != mac_code:
                #     self.show_dialog()
                #     return
        # except FileNotFoundError:
        #     print(f"文件 '{cfg_path}' 未找到.")
        #     return
        # except Exception as e:
        #     print(f"发生错误: {str(e)}")
        #     return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", ".", "Image Files (*.png)"
        )

        if not file_path:
            print("未指定图像路径，请选择一个图像")
            return

        img_np = io.imread(file_path)
        if len(img_np.shape) == 2:
            img_3c = np.repeat(img_np[:, :, None], 3, axis=-1)
        else:
            img_3c = img_np


        self.img_3c = img_3c

        self.update_image()


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('img/11.png'))  # 设置应用程序图标
app.setApplicationName("中国矿业大学-徐州市第一人民医院无灌注区智能识别软件（大模型识别模式）")  # 设置应用程序名称
w = Window()
w.show()
sys.exit(app.exec_())
