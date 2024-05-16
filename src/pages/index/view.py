from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from qfluentwidgets import *

from .app_info import AppInfoCard
from .gallary import GalleryCard
from .clock import ClockCard
from .basic_info import BasicInfoCard

class IndexView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('IndexView')

        self.appInfoCard = AppInfoCard(self)
        self.appInfoCard.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        
        self.galleryCard = GalleryCard(self)
        self.galleryCard.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.clockCard = ClockCard(self)
        self.clockCard.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.basicInfoCard = BasicInfoCard(self)

        self.initLayout()


    def initLayout(self):
        vLayout = QVBoxLayout()
        vLayout.setAlignment(Qt.AlignTop)

        vLayout.addWidget(self.appInfoCard)
        vLayout.addWidget(self.galleryCard)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.clockCard)
        hLayout.addWidget(self.basicInfoCard)
        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)

