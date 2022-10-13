from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from UI_Widgets.parameter_input_widget import *
from parameters import *


class ParameterInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('UIs\InputWindow.ui',self)
        self.current_patient = Patient()
        self.save_btn.clicked.connect(lambda: self.save_data())
        self.open_btn.clicked.connect(lambda: self.load_data())

    def load_data(self, patient = get_TEST_PATIENT()):
        self.personal_info_table.setItem(0,0, QTableWidgetItem(str(patient.surname)))
        self.personal_info_table.setItem(1,0, QTableWidgetItem(str(patient.name)))
        self.personal_info_table.setItem(2,0, QTableWidgetItem(str(patient.patronymic)))

        table =self.main_table
        for row, param_key in enumerate(patient.main_parameters):
            line = patient.main_parameters[param_key]
            #print(key, line)
            for col, col_key in enumerate(line):
                str_item = str(patient.main_parameters[param_key][col_key])
                table.setItem(row,col, QTableWidgetItem(str_item))

    def save_data(self):
        #test_patient = get_TEST_PATIENT()

        table =self.main_table

        print(table.item(0,1).text())









    def create_paraneters_list(self):
        lay = QVBoxLayout()
        self.parameters = []
        for line in range(10):
            param = ParameterInputLineWidget(f'Парам{line}')
            self.parameters.append(param)
            lay.addWidget(param)

        return lay



