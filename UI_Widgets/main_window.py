import os
from PyQt5.QtWidgets import *
from UI_Widgets.input_window import *
from  PyQt5.uic import loadUi
from diagrams import *
from DB_Module.db_module import *
from UI_Widgets.CreatePatient_window import CreatePatientWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui',self)
        self.child_windows = []
        self.create_patient_btn.clicked.connect(lambda :self.create_new_patient())

        self.show()


    def create_new_patient(self):
        creation_win = CreatePatientWindow()
        self.child_windows.append(creation_win)
        creation_win.show()
        return

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