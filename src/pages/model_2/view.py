from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from .toolbar import Toolbar
from .image_manipulate import ImageManipulatePanel
from .image_selector import ImageSelectorPanel
from .patient_info import PatientInfoPanel
from .result_info import ResultInfoPanel
from .model import Model, Painter

class Model2View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('Model2View')
        self.setStyleSheet('background-color: blue;')
    
        self.toolbar = Toolbar(self,Painter)
        self.toolbar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.imagePanel = ImageManipulatePanel()
        self.imagePanel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.hInfoPanels = QHBoxLayout()
        self.imageSelector = ImageSelectorPanel()
        self.patientInfoPanel = PatientInfoPanel()
        self.resultInfoPanel = ResultInfoPanel()

        self.initLayout()

    def initLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.imagePanel)

        self.hInfoPanels.addWidget(self.imageSelector)
        self.hInfoPanels.addWidget(self.patientInfoPanel)
        layout.addLayout(self.hInfoPanels)

        self.setLayout(layout)