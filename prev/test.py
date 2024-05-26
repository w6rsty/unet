import sys

from PyQt5.QtCore import QTimer, QDateTime, QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QApplication
from qfluentwidgets import CardWidget, TransparentToolButton, ProgressRing, BodyLabel, CaptionLabel


class dateTime_panel(CardWidget):
	"""
	时间组件
	"""

	def __init__(self, p=None):
		super(dateTime_panel, self).__init__(p)
		self.ui_init()
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
		self.date_lable.setText(str_dt)
		self.time_label.setText(time)
		self.hourRing.setValue(int(h))
		self.minRing.setValue(int(m))
		self.secRing.setValue(int(s))

	def ui_init(self):
		self.setMaximumSize(QSize(400, 280))
		self.setFixedHeight(280)
		self.setMinimumWidth(350)
		self.layout = QVBoxLayout()
		self.layout.setSpacing(5)
		self.word_btn = TransparentToolButton(self)
		self.word_btn.setText("时间卡片 >")
		self.hourRing = ProgressRing(self)
		self.hourRing.setMinimum(0)
		self.hourRing.setMaximum(24)
		self.hourRing.setStrokeWidth(10)

		hour_layout = QVBoxLayout(self.hourRing)
		self.minRing = ProgressRing(self.hourRing)
		self.minRing.setMinimum(0)
		self.minRing.setMaximum(60)
		self.minRing.setStrokeWidth(10)
		hour_layout.addWidget(self.minRing)
		hour_layout.setAlignment(self.minRing, Qt.AlignCenter)

		min_layout = QVBoxLayout(self.minRing)
		self.secRing = ProgressRing(self.minRing)
		self.secRing.setMinimum(0)
		self.secRing.setMaximum(60)
		self.secRing.setStrokeWidth(10)
		self.hourRing.setCustomBarColor("#0033FF", "#3366FF")
		self.minRing.setCustomBarColor("#009900", "#66CC66")
		self.hourRing.setFixedSize(QSize(150, 150))
		self.minRing.setFixedSize(QSize(120, 120))
		self.secRing.setFixedSize(QSize(90, 90))
		min_layout.addWidget(self.secRing)
		min_layout.setAlignment(self.secRing, Qt.AlignCenter)

		self.date_lable = BodyLabel(self)
		hover_layout = QVBoxLayout(self.secRing)
		self.time_label = BodyLabel(self.secRing)
		hover_layout.addWidget(self.time_label)
		hover_layout.setAlignment(self.time_label, Qt.AlignCenter)

		self.layout.addWidget(self.word_btn)
		self.layout.addWidget(self.hourRing)
		self.layout.addWidget(self.date_lable)
		self.layout.setAlignment(self.hourRing, Qt.AlignCenter)
		self.layout.setAlignment(self.date_lable, Qt.AlignCenter)
		self.setLayout(self.layout)

if __name__ == '__main__':
	QApplication.setHighDpiScaleFactorRoundingPolicy(
		Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
	app = QApplication(sys.argv)
	w = dateTime_panel()
	w.show()
	app.exec_()

