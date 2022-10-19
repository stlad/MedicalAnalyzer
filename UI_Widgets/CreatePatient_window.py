import os
from PyQt5.QtWidgets import *
from UI_Widgets.input_window import *
from UI_Widgets.main_window import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *


class CreatePatientWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('UIs\CreatePatient.ui',self)
        self.save_btn.clicked.connect(lambda: self.save_patient_to_db())


    def parameter_check(self):
        return self.name_edit.text() !='' and self.surname_edit.text() !=''

    def save_patient_to_db(self):
        if(not self.parameter_check()):
            print('не корректно')
            return

        cur = CON.con.cursor()
        a = self.name_edit.text()
        b = self.surname_edit.text()
        c = self.patron_edit.text()
        d = self.phone_edit.text()
        sql = ''.join([
            f"Insert into patient(Name, Surname, Patronymic, Phone_number) ",
            f"values('{self.name_edit.text()}','{self.surname_edit.text()}','{self.patron_edit.text()}','{self.phone_edit.text()}')"
            ])
        cur.execute(sql)

        CON.con.commit()
        #СДЕЛАТЬ ЗАВЕРШЕНИЕ ОКНА


