from PyQt5.QtWidgets import QWidget, QVBoxLayout    
from PyQt5.QtCore import Qt, QTimer, QDateTime
from qfluentwidgets import *

class ClockCard(HeaderCardWidget):
    """时间卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("时间卡片")
        self.setupUI()
        self.timer_init()
        self.timer.start()

    def timer_init(self):
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        qdt = QDateTime.currentDateTime()
        str_dt, time = qdt.toString("yyyy-MM-dd hh:mm:ss").split(" ")
        h, m, s = time.split(":")
        self.dateLabel.setText(str_dt)
        self.timeLabel.setText(time)
        self.hourRing.setValue(int(h))
        self.minRing.setValue(int(m))
        self.secRing.setValue(int(s))

    def setupUI(self):
        self.clock = QWidget()
        self.clockLayout = QVBoxLayout(self.clock)
        self.clockLayout.setAlignment(Qt.AlignCenter)

        self.face = QWidget(self.clock)
        self.faceLayout = QVBoxLayout(self.face)
        self.faceLayout.setAlignment(Qt.AlignCenter)

        self.hourRing = ProgressRing(self.face)
        self.hourRing.setRange(0, 24)
        self.hourRing.setStrokeWidth(10)
        self.hourRing.setFixedSize(160, 160)
        self.hourRing.setCustomBarColor("#0033FF", "#3366FF")
        hourLayout = QVBoxLayout(self.hourRing)
        hourLayout.setAlignment(Qt.AlignCenter)

        self.minRing = ProgressRing(self.face)
        self.minRing.setRange(0, 60)
        self.minRing.setStrokeWidth(10)
        self.minRing.setFixedSize(130, 130)
        self.minRing.setCustomBarColor("#009900", "#66CC66")
        hourLayout.addWidget(self.minRing)
        minLayout = QVBoxLayout(self.minRing)
        minLayout.setAlignment(Qt.AlignCenter)
        
        self.secRing = ProgressRing(self.face)
        self.secRing.setRange(0, 60)
        self.secRing.setStrokeWidth(10)
        self.secRing.setFixedSize(100, 100)
        minLayout.addWidget(self.secRing)

        self.faceLayout.addWidget(self.hourRing)

        self.dateLabel = TitleLabel(self.clock)
        self.timeLabel = LargeTitleLabel(self.clock)

        self.clockLayout.addWidget(self.face, 2)
        self.clockLayout.addWidget(self.dateLabel, 1, Qt.AlignCenter)
        self.clockLayout.addWidget(self.timeLabel, 1, Qt.AlignCenter)

        self.vBoxLayout.addWidget(self.clock)
    