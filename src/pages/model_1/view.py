from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog
import json
import os

import config as cfg
from .toolbar import Toolbar
from .image_manipulate import ImageManipulatePanel
from .image_selector import ImageSelectorPanel
from .patient_info import PatientInfoPanel
from .result_info import ResultInfoPanel
from .model import Model, Painter
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
        ###############################################
        self.imagePanel = ImageManipulatePanel(self.jsonLibrary, self.currentOperationMode)
        self.imagePanel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.hInfoPanels = QHBoxLayout()
        self.patientInfoPanel = PatientInfoPanel(self.jsonLibrary)
        self.resultInfoPanel = ResultInfoPanel(self.jsonLibrary)
        self.imageSelector = ImageSelectorPanel(self.imagePanel, self.patientInfoPanel, self.resultInfoPanel, self)

        self.model = Model(cfg.LARGE_MODEL_PATH)
        self.painter = Painter(self.model)

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

    # 加载图片
    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, '选择图片', './', 'Images(*.png *.jpg *.jpeg *.bmp *.gif)')[0]
        if not path:
            print('未指定图像路径，请选择一个图像')
            return
        
        self.currentImagePath = path
        self.imagePanel.setImageByPath(path)


    # 读取历史
    def readHistory(self):
        self.loadImage()

    # 大图识别(识别整个图片， 使用log4)
    def globalRecognize(self):
        print("大图识别")
        pass
    
    # 矩形增加(添加矩形识别区域)
    def addRect(self):
        print("当前模式: 矩形增加")
        self.currentOperationMode = OperationMode.ADD_RECT

    # 矩形删除(删除矩形识别区域)
    def deleteRect(self):
        print("当前模式: 矩形删除")
        self.currentOperationMode = OperationMode.DELETE_RECT

    # 手动添加(手动添加标注区域)
    def manualAdd(self):
        print("当前模式: 手动添加")
        self.currentOperationMode = OperationMode.MANUAL_ADD

    # 手动删除(手动删除标注区域)
    def manualDelete(self):
        print("当前模式: 手动删除")
        self.currentOperationMode = OperationMode.MANUAL_DELETE

    # 区域生长
    def regionGrow(self):
        print("当前模式: 区域生长")
        self.currentOperationMode = OperationMode.REGION_GROW

    # 眼底分区
    def retinaSeg(self):
        print("当前模式: 眼底分区")
        self.currentOperationMode = OperationMode.RETINA_SEG

    # 矩形占比(
    def rectRatio(self):
        print("当前模式: 矩形占比")
        self.currentOperationMode = OperationMode.RECT_RATIO

    # 撤销操作(撤销上一步操作)
    def undo(self):
        if self.historyStack.count > 0:
            self.historyStack.pop()
            # 重绘
            self.imagePanel.update()

    # 数据保存
    def saveData(self):
        print("保存数据")
        pass

    # 掩膜保存
    def saveMask(self):
        print("保存掩膜")
        pass


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