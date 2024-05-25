from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog
import json
import os

import config as cfg
from .toolbar import Toolbar
from .image_manipulate import ImageManipulatePanel
from .image_selector import ImageSelectorPanel
from .patient_info import PatientInfoPanel
from .result_info import ResultInfoPanel
from .model import Model
from .image_manipulate import OperationMode

class Model1View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Model1View')

        self.jsonLibrary = JsonLibrary(cfg.JSON_DIR)

        ###############################################
        # 状态变量

        # 当前图片的路径(可能用于保存路径)
        self.currentImagePath = None
        # 历史操作栈, 用于撤销操作
        self.historyStack = []

        # 当前操作模式
        self.currentOperationMode = OperationMode.NONE

        # 加载模型
        self.model = Model()
        ###############################################
        self.imagePanel = ImageManipulatePanel(self.jsonLibrary, self.model, self.currentOperationMode)
        self.imagePanel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.hInfoPanels = QHBoxLayout()
        self.patientInfoPanel = PatientInfoPanel(self.jsonLibrary)
        self.resultInfoPanel = ResultInfoPanel(self.jsonLibrary)
        self.imageSelector = ImageSelectorPanel(self.imagePanel, self.patientInfoPanel, self.resultInfoPanel, self)


        self.toolbar = Toolbar(self.model, self)
        self.toolbar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.toolbar, 1)
        layout.addWidget(self.imagePanel, 3)

        self.hInfoPanels.setSpacing(10)
        self.hInfoPanels.addWidget(self.imageSelector)
        self.hInfoPanels.addWidget(self.patientInfoPanel)
        self.hInfoPanels.addWidget(self.resultInfoPanel)
        layout.addLayout(self.hInfoPanels, 1)

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