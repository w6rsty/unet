import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from .pages.navigation.view import MainWindow

def main(args):
    app = QApplication(args)
    app.processEvents()


    mainWindow = MainWindow()
    mainWindow.showMaximized()

    sys.exit(app.exec())