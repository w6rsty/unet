import sys
from PyQt5.QtCore import Qt, QSize, QUrl
import subprocess  # 确保这行导入位于文件的顶部
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import *


class Demo(MSFluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(TitleBar(self))
        self.detailedInterface = DetailInterface(self)

        self.resize(1000, 800)
        self.setWindowTitle('慧眼卫视”——AI驱动的眼底图像智能处理软件')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.addSubInterface(self.detailedInterface, FluentIcon.HOME,
                             '主页', selectedIcon=FluentIcon.HOME_FILL)
        self.navigationInterface.addItem('app', FluentIcon.ALBUM, '无灌注区域识别', onClick=lambda: self.onAppClicked())

        self.navigationInterface.addItem('video', FluentIcon.VIDEO, '糖网分级', onClick=lambda: self.onAppClicked1())
        
        self.navigationInterface.addItem('sync', FluentIcon.SYNC, '血网分割', onClick=lambda: self.onAppClicked2())

        self.navigationInterface.addItem(
            'lib', FluentIcon.BOOK_SHELF, '库', position=NavigationItemPosition.BOTTOM, selectedIcon=FluentIcon.LIBRARY_FILL)
        self.navigationInterface.addItem(
            'help', FluentIcon.HELP, '帮助', position=NavigationItemPosition.BOTTOM) 

        self.stackedWidget.setStyleSheet('QWidget{background: transparent}')
        
    def onAppClicked(self):
          filepath = "wuguan.py"
          subprocess.Popen(['python', filepath])
          print("应用被点击")
    def onAppClicked1(self):
          filepath = "wuguan.py"
          subprocess.Popen(['python', filepath])
          print("应用被点击")
    def onAppClicked2(self):
          filepath = "wuguan.py"
          subprocess.Popen(['python', filepath])
          print("应用被点击")


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


class AppInfoCard(SimpleCardWidget):
    """ App information card """

    def __init__(self, parent=None):
        super().__init__(parent)
        # FIXME: relative path
        self.iconLabel = ImageLabel("C:/Users/Administrator/Desktop/1.png", self)
        self.iconLabel.setBorderRadius(8, 8, 8, 8)
        self.iconLabel.scaledToWidth(120)

        self.nameLabel = TitleLabel('慧眼卫视', self)
        self.installButton = PrimaryPushButton('详细', self)
        self.companyLabel = HyperlinkLabel(
            QUrl('https://www.xzsdyyy.com/'), '第一人民医院 Inc.', self)
        self.installButton.setFixedWidth(160)

        self.scoreWidget = StatisticsWidget('平均准确度', '97.2', self)
        self.separator = VerticalSeparator(self)
        self.commentWidget = StatisticsWidget('已测试数', '300', self)

        self.descriptionLabel = BodyLabel(
            '”慧眼卫视“——AI驱动的眼底图像智能处理软件', self)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setStyleSheet('QLabel {padding-right: 125px}')

        self.tagButton = PillPushButton('组件库', self)
        self.tagButton.setCheckable(False)
        setFont(self.tagButton, 12)
        self.tagButton.setFixedSize(80, 32)

        self.shareButton = TransparentToolButton(FluentIcon.SHARE, self)
        self.shareButton.setFixedSize(32, 32)
        self.shareButton.setIconSize(QSize(15, 15))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.initLayout()

    def initLayout(self):
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # name label and install button
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.nameLabel)
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

        # button
        self.vBoxLayout.addSpacing(12)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.tagButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.shareButton, 0, Qt.AlignRight)
        

class TitleBar(MSFluentTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.lineEdit = SearchLineEdit(self)
        self.lineEdit.setPlaceholderText('')
        self.lineEdit.setClearButtonEnabled(True)

        self.avatarButton = TransparentToolButton('resource/shoko.png', self)
        self.avatarButton.setIconSize(QSize(28, 28))
        self.avatarButton.setFixedSize(28, 28)

    def resizeEvent(self, e):
        w, h = self.width(), self.height()
        self.avatarButton.move(w - 205, h//2-self.avatarButton.height()//2)

        self.lineEdit.resize(w // 2, self.lineEdit.height())
        self.lineEdit.move(w//2 - self.lineEdit.width()//2, h//2-self.lineEdit.height()//2)
        

class ClockCard(HeaderCardWidget):
    """时间卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("时间卡片 >")
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
        self.hourRing.setFixedSize(200, 200)
        self.hourRing.setCustomBarColor("#0033FF", "#3366FF")
        hourLayout = QVBoxLayout(self.hourRing)
        hourLayout.setAlignment(Qt.AlignCenter)

        self.minRing = ProgressRing(self.face)
        self.minRing.setRange(0, 60)
        self.minRing.setStrokeWidth(10)
        self.minRing.setFixedSize(170, 170)
        self.minRing.setCustomBarColor("#009900", "#66CC66")
        hourLayout.addWidget(self.minRing)
        minLayout = QVBoxLayout(self.minRing)
        minLayout.setAlignment(Qt.AlignCenter)
        
        self.secRing = ProgressRing(self.face)
        self.secRing.setRange(0, 60)
        self.secRing.setStrokeWidth(10)
        self.secRing.setFixedSize(140, 140)
        minLayout.addWidget(self.secRing)

        self.faceLayout.addWidget(self.hourRing)

        self.dateLabel = TitleLabel(self.clock)
        self.timeLabel = LargeTitleLabel(self.clock)

        self.clockLayout.addWidget(self.face, 2)
        self.clockLayout.addWidget(self.dateLabel, 1, Qt.AlignCenter)
        self.clockLayout.addWidget(self.timeLabel, 1, Qt.AlignCenter)

        self.vBoxLayout.addWidget(self.clock)
    

class GalleryCard(HeaderCardWidget):
    """ Gallery card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('屏幕截图')

        self.flipView = HorizontalFlipView(self)
        self.expandButton = TransparentToolButton(
            FluentIcon.CHEVRON_RIGHT_MED, self)

        self.expandButton.setFixedSize(32, 32)
        self.expandButton.setIconSize(QSize(12, 12))

        self.flipView.addImages([
            'img/1212.jpg', 'img/11111.jpg', 'img/ceshi.jpg',
            'img/ceshi1.jpg',
        ])
        self.flipView.setBorderRadius(8)
        self.flipView.setSpacing(10)
        self.flipView.setItemSize(QSize(620, 351))
        self.flipView.setMinimumSize(QSize(620, 351))

        self.headerLayout.addWidget(self.expandButton, 0, Qt.AlignRight)
        self.viewLayout.addWidget(self.flipView)


class BasicInfoCard(HeaderCardWidget):
    """信息卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('信息')
        
        label = QLabel(
'''慧眼卫视基于深度学习和智能优化算法等先进技术，有针对性地改进了医学影像信息系统中存在的缺点和不足之处。集成了医学图像处理、图像可视化、病灶自动定位等功能，实现了医学图像自动识别、自动标注、自动定位全过程。
    - 限1人使用
    - 可以在多台设备通过账号登陆同时使用
    - 适用于PC
    - 适用于windows7以上操作系统
    - 1TB(1.000 GB)安全云存储空间
    - 使用Docker技术进行模块化和容器化部署云服务后台
    - 针对图像数据和分析数据进行高级安全存储
    - 包括无灌注区域识别工具、糖网分级工具和血网分割工具
    - 直观简洁，且易于使用，任何人都可以轻松操作''')
        self.viewLayout.addWidget(label, 0, Qt.AlignTop | Qt.AlignLeft)


class DetailInterface(SingleDirectionScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.appInfoCard = AppInfoCard(self)
        self.galleryCard = GalleryCard(self)

        self.cardsRow = QWidget(self)  # Horizontal container for ClockCard and RightSideCard
        self.cardsRowLayout = QHBoxLayout(self.cardsRow)
        
        self.customCard = ClockCard(self)
        self.rightSideCard = BasicInfoCard(self)  # Create an instance of the right side card

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('detailedInterface')

        self.vBoxLayout.addWidget(self.appInfoCard, 1)
        self.vBoxLayout.addWidget(self.galleryCard, 2)
        self.vBoxLayout.addWidget(self.cardsRow, 2)
        
        self.cardsRowLayout.addWidget(self.customCard, 1)
        self.cardsRowLayout.addWidget(self.rightSideCard, 3)

        self.view.setStyleSheet('QWidget {background:transparent}')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建启动界面，使用应用图标作为启动图片
    splash_pix = QPixmap('assets/pics/paper.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()  # 处理初始化过程中的事件

    w = Demo()

    # 使用 QTimer.singleShot 来延迟关闭启动界面和显示主窗口
    # TODO: change when release
    QTimer.singleShot(100, lambda: (splash.finish(w), w.showFullScreen()))  # 使用 showFullScreen() 代替 show()

    sys.exit(app.exec_())

