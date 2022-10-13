import sys
from PyQt5.QtWidgets import *
from UI_Widgets import main_window

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = main_window.MainWindow()
    sys.exit(app.exec_())
