from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon

from qfluentwidgets import SingleDirectionScrollArea, FlowLayout

import os 
import config as cfg

class ImageSelectorPanel(QWidget):
    def __init__(self, manipulated, patient_info, result_info,gridlayout, dispatch, parent=None):
        super().__init__(parent)
    
        self.imageButtons = []
        for index, path in enumerate(cfg.DEMO_IMAGE_PATHS):
            bt = ImageButton(index, path, manipulated, patient_info, result_info)
            self.imageButtons.append(bt)
            
        self.addButton = ImageButton(-1, cfg.ADD_ICON_PATH)
        self.addButton.setCallBack(dispatch.imagePanel.loadImage)
        
        
        gridlayout.addWidget(self.imageButtons[0],0,0)
        gridlayout.addWidget(self.imageButtons[1],0,1)
        gridlayout.addWidget(self.imageButtons[2],0,2)
        gridlayout.addWidget(self.imageButtons[3],1,0)
        gridlayout.addWidget(self.imageButtons[4],1,1)
        gridlayout.addWidget(self.addButton,1,2)
        
    #     self.initLayout()

    # def initLayout(self):
    #     layout = FlowLayout(self, needAni = False)
    #     layout.setSpacing(20)

    #     for bt in self.imageButtons:
    #         layout.addWidget(bt)

    #     layout.addWidget(self.addButton)

    #     self.setLayout(layout)
        
    

class ImageButton(QPushButton):
    def __init__(self, id, path, manipulated = None, patient_info = None, result_info = None, parent=None):
        super().__init__(parent)

        self.id = id

        self.setIcon(QIcon(os.path.abspath(path)))
        self.setIconSize(QSize(200, 180))
        # self.initLayout()

        self.manipulated = manipulated
        self.patient_info = patient_info
        self.result_info = result_info
        if (id >= 0):
            self.clicked.connect(lambda: self.notify(id))

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def notify(self, id):
        if self.patient_info is not None:
            self.patient_info.set_data(id)
        if self.result_info is not None:
            self.result_info.set_data(id)
        if self.manipulated is not None:
            self.manipulated.setImage(id)
    
    def setCallBack(self, callback):
        self.clicked.connect(lambda: callback())