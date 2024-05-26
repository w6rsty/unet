from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplashScreen, QWidget
from PyQt5.QtGui import QIcon, QPixmap

from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow

import src.config as cfg
from ..index.view import IndexView
from ..wuguanzhu.view import WuguanzhuView
from ..tangwang.new_tangwang import Ui_Form
from ..xuewang.view import XuewangView



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
        self.tangwangInterface = WuguanzhuView(self)
        
        self.Form = QWidget()
        ui = Ui_Form()
        ui.setupUi(self.Form)

        self.xuewangInterface = XuewangView(self)

        self.addSubInterface(self.indexInterface, FIF.HOME, '主页')
        self.addSubInterface(self.tangwangInterface, FIF.ALBUM, '无灌注识别')
        self.addSubInterface(self.Form, FIF.VIDEO, '糖网分级')
        self.addSubInterface(self.xuewangInterface, FIF.PHOTO, '血网分割')
