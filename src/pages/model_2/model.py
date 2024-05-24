from PyQt5.QtWidgets import QLabel, QGraphicsScene, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt
from skimage import io
import numpy as np
from PIL import Image
from .unet import Unet

img_2c = None

class Model:
    def __init__(self, path, use_cuda=False):
        self.model_path = path
        self.num_classes = 2
        self.model = Unet(model_path=self.model_path, num_classes=self.num_classes, input_shape=[1024, 1024], cuda=use_cuda)
        
    def get(self):
        return self.model

class Painter(QLabel):
    def __init__(self, model, parent=None):
        super(Painter, self).__init__(parent)
        global img_2c
        self.is_mouse_down = True
        self.img_3c = img_2c
        self.initial_image = None
        self.start_pos = None
        self.last_pos = None
        self.mode = "draw"
        self.scene = None
        self.half_point_size = 5
        self.point_size = 10
        self.scene = QGraphicsScene(self)
        self.coordinate_history = []
        self.history = []
        self.line_width = 5
        self.color_idx = 0
        self.tag = 0
        self.rect = None
        self.initial_image = None
        self.mask_c = np.zeros((100, 100, 3), dtype=np.uint8)

        self.model = model

    def load_image(self):
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

            self.set_image(img_3c)
            self.initial_image = np.copy(img_3c)  # 将self.initial_image赋值为加载的图像
    def set_image(self, img_3c):
        q_img = QImage(img_3c.data, img_3c.shape[1], img_3c.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.setPixmap(pixmap)
        
    def set_initial_image(self, image):
            # 这里可以直接使用 global initial_image
            global initial_image
            initial_image = image
            self.set_image(initial_image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_down = True
            x, y = event.pos().x(), event.pos().y()  # 使用 event.pos() 获取鼠标位置
            self.start_pos = (x, y)

        try:
            if self.mode == "draw":
                # 处理绘制逻辑
                self.is_mouse_down = True
                self.start_pos = event.pos()  # 使用 event.pos() 获取鼠标位置
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
                self.start_pos = event.pos()  # 使用 event.pos() 获取鼠标位置
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
                self.start_pos = event.pos()  # 使用 event.pos() 获取鼠标位置
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
                # 处理描述模式逻辑
                self.is_mouse_down = True
                self.drawing = True
                self.points = [event.pos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
            elif self.mode == "delete":
                # 处理删除模式逻辑
                self.is_mouse_down = True
                self.deleteing = True
                self.points = [event.pos()]
                self.tag = 0
                self.history.append(np.copy(self.img_3c))
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def mouseMoveEvent(self, event):
        if self.is_mouse_down:
            self.current_pos = event.pos()
            if self.mode in ["describe", "delete"]:
                self.points.append(event.pos())
            self.update()
    def mouseReleaseEvent(self, event):
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
        if event.button() == Qt.LeftButton:
            self.is_mouse_down = False
            global img_2c
            # print("img2c",img_2c)
            if self.mode == "draw":
                self.img_3c=img_2c
                img_3c=self.img_3c
                color = colors[self.color_idx]
                x = int(min(self.start_pos.x(), event.pos().x()))
                y = int(min(self.start_pos.y(), event.pos().y()))
                width = int(abs(self.start_pos.x() - event.pos().x()))
                height = int(abs(self.start_pos.y() - event.pos().y()))

                self.mask_c[y: y + height, x: x + width] = color
                self.color_idx = (self.color_idx + 1) % len(colors)

                xmin = int(min(self.start_pos.x(), event.pos().x()))
                xmax = int(max(self.start_pos.x(), event.pos().x()))
                ymin = int(min(self.start_pos.y(), event.pos().y()))
                ymax = int(max(self.start_pos.y(), event.pos().y()))

                region_to_render_white = initial_image[ymin:ymax, xmin:xmax]
                # print(initial_image)
                # if region_to_render_white.shape[0] > 600  and region_to_render_white.shape[1] > 600:
                image = Image.fromarray(initial_image)
                image.save('output_image.png')
                # TODO: Detect the image here
                # segmented_image = unet_instance1.detect_image(image)
                segmented_image = self.model.detect_image(image)
                image_array = np.array(segmented_image)
                # print(image_array)
                img_3c = image_array
                self.img_3c=img_3c.copy()
                # print(self.img_3c[ymin:ymax, xmin:xmax])
                # elif region_to_render_white.shape[0] < 1  and region_to_render_white.shape[1] <1:
                #     return
                # else:
                #     image = Image.fromarray(region_to_render_white)
                #     segmented_image = unet_instance.detect_image(image)
                #     image_array = np.array(segmented_image)
                #     self.img_3c[ymin:ymax, xmin:xmax] = image_array
                self.update_image()

            elif self.mode == "difference":
                xmin = int(min(self.start_pos.x(), event.pos().x()))
                xmax = int(max(self.start_pos.x(), event.pos().x()))
                ymin = int(min(self.start_pos.y(), event.pos().y()))
                ymax = int(max(self.start_pos.y(), event.pos().y()))
                self.show_difference_percentage(xmin, xmax, ymin, ymax)

            elif self.mode == "restore":
                xmin = int(min(self.start_pos.x(), event.pos().x()))
                xmax = int(max(self.start_pos.x(), event.pos().x()))
                ymin = int(min(self.start_pos.y(), event.pos().y()))
                ymax = int(max(self.start_pos.y(), event.pos().y()))

                region_to_restore = self.initial_image[ymin:ymax, xmin:xmax]
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
                    if len(self.points) >= 3:
                        start_point = self.points[0]
                        end_point = self.points[-1]

                    self.drawEdge(start_point, end_point)
                    self.deleteMask()
                except Exception as e:
                    print(e)
            

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.start_pos and hasattr(self, 'current_pos'):
            # Use QPoint methods to get coordinates
            spx, spy = self.start_pos.x(), self.start_pos.y()
            cpx, cpy = self.current_pos.x(), self.current_pos.y()

            rect_color = QColor("red")
            if self.mode == "difference":
                rect_color = QColor("yellow")
            elif self.mode == "restore":
                rect_color = QColor("green")

            painter.setPen(QPen(rect_color, 3))
            painter.drawRect(spx, spy, cpx - spx, cpy - spy)
            
    def update_image(self):
        if hasattr(self, 'img_3c'):  # 检查是否存在 img_3c 属性
            # 将 numpy 数组（self.img_3c）转换为 QImage 对象
            height, width, channels = self.img_3c.shape
            bytes_per_line = channels * width
            image = QImage(self.img_3c.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # 将 QImage 转换为 QPixmap 用于在 GUI 中显示
            pixmap = QPixmap.fromImage(image)

            # 根据 DrawingLabel 的当前尺寸调整 QPixmap 的大小，以填充整个 Label
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # 设置调整大小后的 QPixmap 到当前的 QLabel（DrawingLabel）
            self.setPixmap(scaled_pixmap)

            # 更新 GUI 以反映更改
            self.update()