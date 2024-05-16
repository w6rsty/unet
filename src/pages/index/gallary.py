from PyQt5.QtCore import Qt
from qfluentwidgets import HeaderCardWidget, HorizontalFlipView

class GalleryCard(HeaderCardWidget):
    """ Gallery card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('屏幕截图')

        self.flipView = HorizontalFlipView(self)
        self.flipView.addImages([
            'img/1212.jpg', 'img/11111.jpg', 'img/ceshi.jpg',
            'img/ceshi1.jpg',
        ])
        
        self.flipView.setBorderRadius(8)
        self.flipView.setSpacing(10)
        # Prevent the image from being stretched
        self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        self.viewLayout.addWidget(self.flipView)
