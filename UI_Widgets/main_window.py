import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *
from UI_Widgets.Analysis_Window import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui', self)
        self.child_windows = []

        self.patients = []
        self.current_patient_id = 0
        self.current_analysis_id = 0
        self.analysis = []

        self.refresh_all_lists()
        self.patient_create_btn.clicked.connect(lambda :self.open_patient_creation())
        self.patient_delete_btn.clicked.connect(lambda: self.delete_chosen_patient())
        self.patient_select_btn.clicked.connect(lambda: self.get_selected_patient_id())
        self.patients_list.currentItemChanged.connect(lambda : self.get_selected_patient_id() )
        self.analysis_create_btn.clicked.connect(lambda :self.create_analysis())
        self.analysis_list.currentItemChanged.connect(lambda: self.get_selected_analysis_id())
        self.analysis_delete_btn.clicked.connect(lambda :self.delete_chosen_analysis())
        self.analisys_select_btn.clicked.connect(lambda:self.open_analysis_creation())
        self.show()

    def refresh_all_lists(self):
        self.refresh_patients_list()
        self.refresh_analysis_list()

    def refresh_patients_list(self):
        """Заполнит таблицу пациентов и вернет их полный список"""
        self.patients_list.clear()
        patients= MainDBController.GetAllPatients()
        self.patients = []
        for pat in patients:
            self.patients.append(pat)
            line = f'{pat[2]} {pat[1]} {pat[3]} {str(pat[4])} |{pat[0]}'
            self.patients_list.addItem(line)

    def refresh_analysis_list(self):
        """Заполнит таблицу анализов и вернет их полный список"""
        if self.current_patient_id == 0:
            return

        self.analysis_list.clear()
        self.analysis = []
        analysis= MainDBController.GetAllAnalysisByPatientID(self.current_patient_id)
        for an in analysis:
            self.analysis.append(an)
            line = f'{an[2]}'
            #print(an)
            self.analysis_list.addItem(line)


    def open_patient_creation(self):
        creation_window = CreatePatientWindow(self)
        self.child_windows.append(creation_window)
        creation_window.show()

    def open_analysis_creation(self):
        patient_index = self.patients_list.currentRow()
        analysis_index = self.analysis_list.currentRow()
        analysis_window = AnalysisWindow(self.patients[patient_index], self.analysis[analysis_index])
        self.child_windows.append(analysis_window)
        analysis_window.show()

    def get_selected_patient_id(self):
        index = self.patients_list.currentRow()
        current_patient = self.patients[index]
        #print(current_patient[0])
        self.current_patient_id = current_patient[0]
        self.refresh_analysis_list()

    def get_selected_analysis_id(self):
        index = self.analysis_list.currentRow()
        current_anal = self.analysis[index]
        self.current_analysis_id = current_anal[0]
        #print(self.current_analysis_id)

    def delete_chosen_patient(self):
        index = self.patients_list.currentRow()
        current_patient = self.patients[index]
        #print(current_patient)
        reply = QMessageBox.question(self, 'Удалить ', f'Удалить пациента {current_patient[1]} {current_patient[2]} {current_patient[3]}?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            MainDBController.DeletePatientById(current_patient[0])
        self.refresh_all_lists()
        return

    def create_analysis(self):
        dialog = QInputDialog(self)
        a_date, ok = dialog.getText(self, 'Введите дату анализа', 'Дата',QLineEdit.Normal)
        a_date = date_text_to_sql_format(a_date)
        if not ok or a_date is None:
            return
        MainDBController.InsertAnalysis([self.current_patient_id, a_date])
        self.refresh_analysis_list()

    def delete_chosen_analysis(self):
        index = self.analysis_list.currentRow()
        current_analysis = self.analysis[index]
        reply = QMessageBox.question(self, 'Удалить ', f'Удалить анализ от {current_analysis[2]}?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            MainDBController.DeleteAnalysisByID(self.current_analysis_id)
        self.refresh_analysis_list()

