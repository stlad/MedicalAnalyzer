from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from UI_Widgets.parameter_input_widget import *
from parameters import *
from diagrams import *

class ParameterInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('UIs\InputWindow.ui',self)
        self.current_patient = Patient() #load_Patient_from_Json('Иванов Иван.json')
        self.save_btn.clicked.connect(lambda: self.save_data())
        self.open_btn.clicked.connect(lambda: self.load_data_from_file())
        self.graph_btn.clicked.connect(lambda:self.get_graphs())
        self.new_patient_btn.clicked.connect(lambda : self.load_new_patient())

    def load_data_from_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);")
        if not fileName:
            print('Error')
            return
        self.current_patient = load_Patient_from_Json(fileName)
        self._fill_main_table_from_current_patient()

    def load_new_patient(self):
        self.current_patient = Patient()
        self._fill_main_table_from_current_patient()

    def _fill_main_table_from_current_patient(self):
        patient = self.current_patient
        self.personal_info_table.setItem(0,0, QTableWidgetItem(str(patient.id)))
        self.personal_info_table.setItem(1,0, QTableWidgetItem(str(patient.surname)))
        self.personal_info_table.setItem(2,0, QTableWidgetItem(str(patient.name)))
        self.personal_info_table.setItem(3,0, QTableWidgetItem(str(patient.patronymic)))

        table =self.main_table
        for row, param_key in enumerate(patient.main_parameters):
            line = patient.main_parameters[param_key]
            for col, col_key in enumerate(line):
                str_item = str(patient.main_parameters[param_key][col_key])
                table.setItem(row,col, QTableWidgetItem(str_item))

    def save_data(self):
        patient = self.current_patient
        self._parameter_table_to_person(self.main_table, patient.main_parameters)
        #self._parameter_table_to_person(self.cytokine_table, patient.cytokine_status)

        patient.id = int(self.personal_info_table.item(0,0).text())
        patient.surname = self.personal_info_table.item(1,0).text()
        patient.name = self.personal_info_table.item(2,0).text()
        patient.patronymic = self.personal_info_table.item(3,0).text()

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "","Json Files (.json);")
        if not fileName:
            print('Error')
            return

        self.current_patient.serialyze_to_json(fileName)

    def _parameter_table_to_person(self, table, patient_param_dct):
        for row, param_key in enumerate(patient_param_dct):
            line = patient_param_dct[param_key]
            for col, col_key in enumerate(line):
                item = table.item(row,col).text()
                try:
                    item=float(item)
                except ValueError:
                    pass
                patient_param_dct[param_key][col_key] = item

        print(patient_param_dct)

    def get_graphs(self):
        patient = self.current_patient
        get_diagrams(f'{patient.surname} {patient.name}.json')




