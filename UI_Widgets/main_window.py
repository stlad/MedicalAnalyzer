import os
from PyQt5.QtWidgets import *
from UI_Widgets.input_window import *
from  PyQt5.uic import loadUi
from diagrams import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui',self)
        self.child_windows = []
        self.input_form_btn.clicked.connect(lambda: self.input_form_window())
        self.graphs_btn.clicked.connect(lambda: self.get_graphs())
        self.show()



    def get_graphs(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);")
        if not fileName:
            print('Error')
            return

        get_diagrams(fileName)

    def input_form_window(self):
        input_win = ParameterInputWindow()
        self.child_windows.append(input_win)
        input_win.show()