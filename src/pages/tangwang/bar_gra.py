import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class BarChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 创建 Matplotlib 图表
        self.figure = plt.figure(figsize=(6, 4))  # 设置图表大小为6x4英寸
        self.canvas = FigureCanvas(self.figure)

        # 在 Matplotlib 图表上绘制条形图
        self.ax = self.figure.add_subplot(111)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def update_chart_data(self, x, y):
        self.ax.clear()
        bars = self.ax.bar(x, y)

        # 在每个柱形上显示相应的数值
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("患者糖网分级概率")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        # 创建包含条形图的 QWidget
        self.bar_chart_widget = BarChartWidget()

        # 将 QWidget 转换为图像，并放置在 QLabel 中
        self.bar_chart_label = QLabel()
        hbox = QHBoxLayout()
        hbox.addWidget(self.bar_chart_widget)
        hbox.setAlignment(Qt.AlignCenter)
        self.bar_chart_label.setLayout(hbox)

        pixmap = self.bar_chart_label.grab()
        self.bar_chart_label.setPixmap(pixmap)

        central_layout.addWidget(self.bar_chart_label)

    def update_chart_data(self, x, y):
        self.bar_chart_widget.update_chart_data(x, y)


def main1(gra):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    # 设置要传递给 BarChartWidget 的新数据
    x = ['零级', '一级', '二级', '三级', '四级']
    y = gra

    mainWindow.update_chart_data(x, y)

    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    gra = [0.1, 0.4, 0.4, 0.25, 0.8]
    main1(gra)
