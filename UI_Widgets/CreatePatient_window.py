import os
from PyQt5.QtWidgets import *
from UI_Widgets.input_window import *
from UI_Widgets.main_window import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *


class CreatePatientWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        loadUi('UIs\CreatePatient.ui',self)
        self.save_btn.clicked.connect(lambda: self.save_patient_to_db())
        self._parent_main_window =parent_window

    def parameter_check(self):
        return self.name_edit.text() !='' and self.surname_edit.text() !=''



    def save_patient_to_db(self):
        if(not self.parameter_check()):
            print('не корректно')
            return

        con = MainBDUser.create_connection_to_DB()
        cur = con.cursor()
        sql = ''.join([
            f"Insert into patient(Name, Surname, Patronymic, Phone_number, Birthday) ",
            f"values('{self.name_edit.text()}','{self.surname_edit.text()}','{self.patron_edit.text()}','{self.phone_edit.text()}', '{ date_text_to_sql_format(self.birthdate_edit.text())}')"
            ])
        cur.execute(sql)

        con.commit()
        con.close()
        self.close()

    def closeEvent(self, event):
        self._parent_main_window.refresh_patient_list()


