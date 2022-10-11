import os, sys
from PyQt5.QtWidgets import *
import  input_form

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = input_form.MainWindow()
    sys.exit(app.exec_())
