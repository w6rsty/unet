from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from qfluentwidgets import HeaderCardWidget

import src.config as cfg

class BasicInfoCard(HeaderCardWidget):
    """信息卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('信息')
        
        label = QLabel(cfg.BASIC_INFO_TEXT)
        # label.setStyleSheet('QLabel {padding-right: 125px}')
        font = QFont('SimHei', 10)
        label.setFont(font)
        self.viewLayout.addWidget(label, 0, Qt.AlignTop | Qt.AlignLeft)
