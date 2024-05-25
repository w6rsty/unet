from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap

from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow

import config as cfg
from ..index.view import IndexView
from ..model_1.view import Model1View
# from ..model_2.new_tangwang import Ui_Form



class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(1920, 1080)
        
        # currentGeometry = self.geometry()  # 获取当前窗口的几何信息
        # print(currentGeometry.width())
        # print(currentGeometry.height())
        self.setWindowIcon(QIcon(cfg.WINDOW_ICON_PATH))

        self.initSplashScreen()
        self.initWindowStyle()
        self.initSubInterfaces()
        # Close splash screen after initialization
        self.splashScreen.finish(self)


    def initSplashScreen(self):
        self.splashScreen = QSplashScreen(QPixmap(cfg.SPLASH_SCREEN_PATH), Qt.WindowStaysOnTopHint)
        self.splashScreen.show()
    
    def initWindowStyle(self):
        self.setWindowTitle(cfg.WINDOW_TITLE)

        self.navigationInterface.setExpandWidth(200)
        
    def initSubInterfaces(self):
        self.indexInterface = IndexView(self)
        self.model1Interface = Model1View(self)
        
        # self.Form = QtWidgets.QWidget()
        # ui = Ui_Form()
        # ui.setupUi(self.Form)

        self.addSubInterface(self.indexInterface, FIF.HOME, '主页')
        self.addSubInterface(self.model1Interface, FIF.ALBUM, '无灌注识别')
        # self.addSubInterface(self.Form, FIF.VIDEO, '模型2')
