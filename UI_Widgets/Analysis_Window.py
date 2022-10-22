import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *

class AnalysisWindow(QWidget):
    def __init__(self, patient:list, analysis:list):
        super().__init__()
        self.patient = patient
        self.analysis = analysis
        print(self.patient)
        print(self.analysis)
        self.initUI()

    def initUI(self):
        loadUi('UIs\AnalysisViewWindow.ui', self)
        self.child_windows = []
        self.fill_patient_info()
        self.catalog = MainDBController.GetAllParameterCatalog()
        self.fill_table_widget_from_catalog()

    def fill_table_widget_from_catalog(self):
        for row,parameter in enumerate(self.catalog):
            print(parameter)
            currentRowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(currentRowCount)
            self.tableWidget.setItem(row,0, QTableWidgetItem(str(parameter[1])))
            self.tableWidget.setItem(row,3, QTableWidgetItem(str(parameter[2])))
            self.tableWidget.setItem(row,4, QTableWidgetItem(str(parameter[3])))
            self.tableWidget.setItem(row,5, QTableWidgetItem(str(parameter[4])))

    def fill_patient_info(self):
        self.surname_edit.setText(self.patient[2])
        self.name_edit.setText(self.patient[1])
        self.patron_edit.setText(self.patient[3])
        self.gender_edit.setText(self.patient[8])
        self.birthday_edit.setText(str(self.patient[4]))
        age = int(self.patient[9].days / 365)
        self.age_edit.setText(f'{age} полных лет')
        self.diag_edit.setText(self.patient[5])
        self.diag_edit_2.setText(self.patient[6])

        a_month = self.analysis[2].month
        if a_month in [3,4,5,6,7,8]: #Это очень плохо, нужно спросить
            season = 'Весна-лето'
        else:
            season = 'Осень-зима'

        self.analysis_date.setText(str(self.analysis[2]))
        self.season_edit.setText(season)