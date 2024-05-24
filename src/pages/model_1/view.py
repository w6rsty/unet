from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import numpy as np
import json
import os

import config as cfg
from .toolbar import Toolbar
from .image_manipulate import ImageManipulatePanel
from .image_selector import ImageSelectorPanel
from .patient_info import PatientInfoPanel
from .result_info import ResultInfoPanel
from .model import Model, Painter


class Model1View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Model1View')

        self.jsonLibrary = JsonLibrary(cfg.JSON_DIR)

        self.imagePanel = ImageManipulatePanel(self.jsonLibrary)
        self.imagePanel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.hInfoPanels = QHBoxLayout()
        self.patientInfoPanel = PatientInfoPanel(self.jsonLibrary)
        self.resultInfoPanel = ResultInfoPanel(self.jsonLibrary)
        self.imageSelector = ImageSelectorPanel(self.patientInfoPanel, self.resultInfoPanel)

        self.model = Model(cfg.MODEL_DATA_PATH)
        self.painter = Painter(self.model)

        self.toolbar = Toolbar(self.model, self.painter)
        self.toolbar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.initLayout()

        #画图相关############################################
        self.circle1 = None
        self.click_point = None
        self.radius = None
        self.end_pos = None
        self.circle = None

        # configs
        self.last_click_pos = None
        self.half_point_size = 5
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
        self.viewLeft = QGraphicsView()
        self.viewRight = QGraphicsView()
        #画图相关############################################

        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)

        # 确保在初始化方法中设置了正确的滚动区域，以便可以滚动查看整个图像
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(3)

        self.pen = QPen(QColor(0, 255, 0))
        self.pen.setWidth(self.slider.value())

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.imagePanel)

        self.hInfoPanels.setSpacing(10)
        self.hInfoPanels.addWidget(self.imageSelector, 1)
        self.hInfoPanels.addWidget(self.patientInfoPanel, 1)
        self.hInfoPanels.addWidget(self.resultInfoPanel, 1)
        layout.addLayout(self.hInfoPanels)

        self.setLayout(layout)

    
class JsonLibrary:
    def __init__(self, dir_path):
        self.dir = dir_path
        self.lib = []
        self.num = 0

        self.load(self.dir);
    
    def load(self, dir):
        for file in os.listdir(dir):
            if file.endswith('.json'):
                with open(os.path.join(dir, file), 'r', encoding="utf-8") as f:
                    self.lib.append(json.load(f))
                    self.num += 1


    def getJsonById(self, id):
        return self.lib[id]