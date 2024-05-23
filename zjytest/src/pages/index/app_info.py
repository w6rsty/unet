from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QFont, QColor
from qfluentwidgets import *

import config as cfg

class AppInfoCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.appName = TitleLabel(cfg.APP_NAME, self)
        self.companyLabel = HyperlinkLabel(QUrl(cfg.COMPANY_URL), cfg.COMPANY_NAME, self)
        self.installButton = PrimaryPushButton('详细', self)
        self.installButton.setFixedWidth(160)

        self.scoreWidget = StatisticsWidget('平均准确度', '97.2', self)
        self.separator = VerticalSeparator(self)
        self.commentWidget = StatisticsWidget('已测试数', '300', self)

        self.descriptionLabel = BodyLabel(cfg.APP_DESCRIPTION, self)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setStyleSheet('QLabel {padding-right: 125px}')

        self.initLayout()

    def initLayout(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # name label and install button
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.appName)
        self.topLayout.addWidget(self.installButton, 0, Qt.AlignRight)

        # company label
        self.vBoxLayout.addSpacing(3)
        self.vBoxLayout.addWidget(self.companyLabel)

        # statistics widgets
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(10)
        self.statisticsLayout.addWidget(self.scoreWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.commentWidget)
        self.statisticsLayout.setAlignment(Qt.AlignLeft)

        # description label
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.descriptionLabel)


class StatisticsWidget(QWidget):
    """ Statistics widget """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom | Qt.AlignHCenter)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))
