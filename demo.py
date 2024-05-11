import sys
from PyQt5.QtCore import Qt, QSize, QUrl
import subprocess  # 确保这行导入位于文件的顶部
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QVBoxLayout, QSpacerItem, QSizePolicy
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
          # FIXME: relative path
          filepath = "D:/unet/wuguan.py"
          subprocess.Popen(['python', filepath])
          print("应用被点击")
    def onAppClicked1(self):
          # FIXME: relative path
          filepath = "D:/unet/wuguan.py"
          subprocess.Popen(['python', filepath])
          print("应用被点击")
    def onAppClicked2(self):
          # FIXME: relative path
          filepath = "D:/unet/wuguan.py"
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
        
class CustomCard(CardWidget):
    """ Custom card example with integrated dateTime functionality """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
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
        self.date_label.setText(str_dt)
        self.time_label.setText(time)
        self.hourRing.setValue(int(h))
        self.minRing.setValue(int(m))
        self.secRing.setValue(int(s))

    def setupUi(self):
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

        self.date_label = BodyLabel(self)
        self.time_label = BodyLabel(self)
        self.layout.addWidget(self.word_btn)
        self.layout.addWidget(self.hourRing)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.time_label)
        self.layout.setAlignment(self.hourRing, Qt.AlignCenter)
        self.layout.setAlignment(self.date_label, Qt.AlignCenter)
        self.layout.setAlignment(self.time_label, Qt.AlignCenter)

        self.setLayout(self.layout)

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


class RightSideCard(HeaderCardWidget):
    """ Gallery card """

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
                 - 直观简洁，且易于使用，任何人都可以轻松操作
            ''')
        self.viewLayout.addWidget(label)


class DetailInterface(SingleDirectionScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.appCard = AppInfoCard(self)
        self.galleryCard = GalleryCard(self)
        self.cardsRow = QWidget(self)  # Container for the horizontal layout of cards
        self.cardsRowLayout = QHBoxLayout(self.cardsRow)
        
        self.customCard = CustomCard(self)
        self.rightSideCard = RightSideCard(self)  # Create an instance of the right side card

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('detailedInterface')

        self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.galleryCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.cardsRow, 0, Qt.AlignTop)
        
        self.cardsRowLayout.addWidget(self.customCard)
        self.cardsRowLayout.addWidget(self.rightSideCard)  # Add the new card to the horizontal layout

        self.view.setStyleSheet('QWidget {background:transparent}')


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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建启动界面，使用应用图标作为启动图片
    splash_pix = QPixmap('D:/unet/paper.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()  # 处理初始化过程中的事件

    w = Demo()

    # 使用 QTimer.singleShot 来延迟关闭启动界面和显示主窗口
    QTimer.singleShot(2000, lambda: (splash.finish(w), w.showFullScreen()))  # 使用 showFullScreen() 代替 show()

    sys.exit(app.exec_())

