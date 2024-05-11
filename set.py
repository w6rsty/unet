import sys
from PyQt5.QtWidgets import QApplication
from predict import Window  # Replace 'your_gui_script' with the actual name of your GUI script file

def main():
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()