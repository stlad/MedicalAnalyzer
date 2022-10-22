import os
from PyQt5.QtWidgets import *
from UI_Widgets.main_window import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from utilits import *


class CreatePatientWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        loadUi('UIs\CreatePatientWindow.ui',self)
        self.save_btn.clicked.connect(lambda:self.save_patient_to_db())
        self._parent_main_window = parent_window

    def save_patient_to_db(self):
        name = self.lineEdit_2.text()
        surname = self.lineEdit_1.text()
        patron = self.lineEdit_3.text()
        birth = date_to_sql_format(self.lineEdit_4.text())
        diag = self.lineEdit_5.text()
        diag2 = self.lineEdit_6.text()
        genes = self.lineEdit_7.text()
        gender = self.lineEdit_8.text()

        if(birth != None):
            MainDBController.InsertPatient([surname,name,patron,birth,diag,diag2,genes,gender])
        self.close()

    def closeEvent(self, event):
        self._parent_main_window.refresh_all_lists()


