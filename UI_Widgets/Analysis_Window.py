import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *
from PyQt5.QtCore import Qt
from utilits import *

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
        self.can_be_editied = True
        self.fill_patient_info()
        self.catalog = MainDBController.GetAllParameterCatalog()
        self.fill_table_widget_from_catalog()
        self.get_parameters()
        self.save_btn.clicked.connect(lambda :self.save_to_db())
        #print(self.params)

    def save_to_db(self):
        result_list = []
        for index,parameter in enumerate(self.catalog):
            deviation = None if self.tableWidget.item(index, 1) == None else self.tableWidget.item(index, 1).text()

            cell = self.tableWidget.item(index, 2)
            if cell == None:
                val = 0
            else:
                try:
                    val = float(cell.text())
                except ValueError:
                    print('В колонке значение должны быть только числа!')
            result_list.append([parameter[0], val, deviation])
        MainDBController.InsertListOfParametersByAnalysisId(self.analysis[0], result_list)

        self.save_btn.setEnabled(False)
        self.is_saved_label.setText('Сохранено')



    def get_parameters(self):
        self.params = MainDBController.GetAllParametersByAnalysisID(self.analysis[0])
        if  len(self.params)==0:
            self.can_be_editied = True
            self.is_saved_label.setText('Не сохранено')
            return
        else:
            self.save_btn.setEnabled(False)
            self.is_saved_label.setText('Сохранено')
            self._fill_table_with_existing_params()

    def _fill_table_with_existing_params(self):
        table = self.tableWidget
        for row, param in enumerate( self.params):
            divation = param[4] if param[4]!='None' else ''
            table.setItem(row,1, QTableWidgetItem(divation))
            table.setItem(row,2, QTableWidgetItem(str(param[2])))

            table.item(row, 1).setFlags(table.item(row, 1).flags() ^ Qt.ItemIsEditable)
            table.item(row, 2).setFlags(table.item(row, 2).flags() ^ Qt.ItemIsEditable)



    def fill_table_widget_from_catalog(self):
        table = self.tableWidget
        for row,parameter in enumerate(self.catalog):
            #print(parameter)
            currentRowCount = self.tableWidget.rowCount()
            table.insertRow(currentRowCount)
            table.setItem(row,0, QTableWidgetItem(str(parameter[1])))
            table.setItem(row,3, QTableWidgetItem(str(parameter[2])))
            table.setItem(row,4, QTableWidgetItem(str(parameter[3])))
            table.setItem(row,5, QTableWidgetItem(str(parameter[4])))
            table.item(row, 0).setFlags(table.item(row, 0).flags() ^ Qt.ItemIsEditable)
            table.item(row, 3).setFlags(table.item(row, 3).flags() ^ Qt.ItemIsEditable)
            table.item(row, 4).setFlags(table.item(row, 4).flags() ^ Qt.ItemIsEditable)
            table.item(row, 5).setFlags(table.item(row, 5).flags() ^ Qt.ItemIsEditable)
        header = table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

    def fill_patient_info(self):
        self.surname_edit.setText(self.patient[2])   #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
        self.name_edit.setText(self.patient[1])      #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
        self.patron_edit.setText(self.patient[3])    #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
        self.gender_edit.setText(self.patient[8])
        self.birthday_edit.setText(date_sql_to_text_format(str(self.patient[4])))
        #print(self.analysis)
        #s = (self.patient[4] -  self.analysis[2])
        age = int((self.analysis[2] - self.patient[4]).days/ 365)
        self.age_edit.setText(f'{age} полных лет')
        self.diag_edit.setText(self.patient[5])
        self.diag_edit_2.setText(self.patient[6])

        a_month = self.analysis[2].month
        if a_month in [3,4,5,6,7,8]: #Это очень плохо, нужно спросить
            season = 'Весна-лето'
        else:
            season = 'Осень-зима'

        self.analysis_date.setText(date_sql_to_text_format(str(self.analysis[2])))
        self.season_edit.setText(season)