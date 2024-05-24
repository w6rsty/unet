import sys
from PyQt5.QtWidgets import QApplication
from pages.navigation.view import MainWindow



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()

    mainWindow = MainWindow()
    mainWindow.showMaximized()
    
    sys.exit(app.exec())