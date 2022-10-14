from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from UI_Widgets.parameter_input_widget import *
from parameters import *


class ParameterInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('UIs\InputWindow.ui',self)
        self.current_patient = get_TEST_PATIENT()
        self.save_btn.clicked.connect(lambda: self.save_data())
        self.open_btn.clicked.connect(lambda: self.load_data())

    def load_data(self):
        patient = self.current_patient
        self.personal_info_table.setItem(0,0, QTableWidgetItem(str(patient.surname)))
        self.personal_info_table.setItem(1,0, QTableWidgetItem(str(patient.name)))
        self.personal_info_table.setItem(2,0, QTableWidgetItem(str(patient.patronymic)))

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

        patient.surname = self.personal_info_table.item(0,0).text()
        patient.name = self.personal_info_table.item(1,0).text()
        patient.patronymic = self.personal_info_table.item(2,0).text()

        #self.current_patient.serialyze_to_json()

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









    def create_paraneters_list(self):
        lay = QVBoxLayout()
        self.parameters = []
        for line in range(10):
            param = ParameterInputLineWidget(f'Парам{line}')
            self.parameters.append(param)
            lay.addWidget(param)

        return lay



