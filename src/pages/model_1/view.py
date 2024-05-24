from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from .toolbar import Toolbar
from .image_manipulate import ImageManipulatePanel
from .image_selector import ImageSelectorPanel
from .patient_info import PatientInfoPanel
from .result_info import ResultInfoPanel
import numpy as np
import json

from .model import Model, Painter

initial_image = None

class Model1View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Model1View')

        # TODO: json library
        
        self.initJson()
        self.imagePanel = ImageManipulatePanel(self.jsonArray)
        self.imagePanel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    

        self.hInfoPanels = QHBoxLayout()
        self.imageSelector = ImageSelectorPanel(self.imagePanel)
        self.patientInfoPanel = PatientInfoPanel(self.jsonArray) # take json lib
        self.resultInfoPanel = ResultInfoPanel(self.jsonArray) # take json lib

        self.initModel()
        self.initPainter()

        self.toolbar = Toolbar(self.model, self.painter)
        self.toolbar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.circle1 = None
        self.click_point = None
        self.radius = None
        self.end_pos = None
        self.circle = None
        global initial_image

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

        # self.view1 = QGraphicsView()
        # self.view2 = QGraphicsView()
        self.img_3c_view1 = None
        self.img_3c_view2 = None
        self.mode = "draw"  # 当前模式，默认为绘制模式


        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.imagePanel)

        self.hInfoPanels.addWidget(self.imageSelector)
        self.hInfoPanels.addWidget(self.patientInfoPanel)
        layout.addLayout(self.hInfoPanels)

        self.setLayout(layout)

    def initModel(self):
        self.model = Model('logs4/best_epoch_weights.pth')

    def initPainter(self):
        self.painter = Painter(self.model)

    def getPainter(self):
        return self.painter

    def initJson(self):
        self.jsonArray = JsonLibrary()
    
class JsonLibrary:
    def __init__(self):
        self.jsonArray = []
        for i in range(1, 5):
            self.jsonArray.append(self.getJson(i))
            print(self.jsonArray[i-1])
    def getJson(self,file_index):
            with open(f'json/json{file_index}.json', 'r',encoding="utf-8") as f:
                json_data = json.load(f)
                return json_data
    
    def getJsonById(self,id):
        return self.jsonArray[id-1]