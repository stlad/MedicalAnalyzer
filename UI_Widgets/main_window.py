import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui', self)
        self.child_windows = []

        self.patients = []
        self.current_patient_id = 0
        self.analysis = []

        self.refresh_all_lists()
        self.patient_create_btn.clicked.connect(lambda :self.open_patient_creation())
        self.patient_delete_btn.clicked.connect(lambda: self.delete_chosen_patient())
        self.patient_select_btn.clicked.connect(lambda: self.get_selected_patient_id())
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
            print(an)
            self.analysis_list.addItem(line)


    def open_patient_creation(self):
        creation_window = CreatePatientWindow(self)
        self.child_windows.append(creation_window)
        creation_window.show()

    def get_selected_patient_id(self):
        index = self.patients_list.currentRow()
        current_patient = self.patients[index]
        print(current_patient[0])
        self.current_patient_id = current_patient[0]
        self.refresh_analysis_list()


    def delete_chosen_patient(self):
        index = self.patients_list.currentRow()
        current_patient = self.patients[index]
        print(current_patient)
        reply = QMessageBox.question(self, 'Удалить ', f'Удалить пациента {current_patient[1]} {current_patient[2]} {current_patient[3]}?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            MainDBController.DeletePatientById(current_patient[0])
        self.refresh_all_lists()
        return

