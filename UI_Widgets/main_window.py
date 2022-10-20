import os
from PyQt5.QtWidgets import *
from UI_Widgets.input_window import *
from  PyQt5.uic import loadUi
from diagrams import *
from DB_Module.db_module import *
from UI_Widgets.CreatePatient_window import CreatePatientWindow
from UI_Widgets.AnalysisForm_window import AnalysisWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui', self)
        self.child_windows = []
        self.create_patient_btn.clicked.connect(lambda :self.create_new_patient())
        self.select_btn.clicked.connect(lambda: self.open_analysis_window())
        self.refresh_patient_list()
        self.load_patients_from_db()
        self.show()


    def create_new_patient(self):
        creation_win = CreatePatientWindow(self)
        self.child_windows.append(creation_win)
        creation_win.show()
        return


    def refresh_patient_list(self):
        self.listWidget.clear()
        patients = self.load_patients_from_db()
        for patient in patients:
            line = f'{patient["id"]} {patient["name"]} {patient["surname"]} {patient["patronymic"]}'
            self.listWidget.addItem(line)


    def load_patients_from_db(self):
        con = MainBDUser.create_connection_to_DB()
        cur = con.cursor()
        sql = "select * from patient"
        cur.execute(sql)
        rows = cur.fetchall()
        res = []
        for row in rows:
            dct_line = {}
            dct_line['id'] = row[0]
            dct_line['name'] = row[1]
            dct_line['surname'] = row[2]
            dct_line['patronymic'] = row[3]
            dct_line['birthday'] = row[4]
            dct_line['city'] = row[5]
            dct_line['phone_number'] = row[6]
            res.append(dct_line)

        return res


    def open_analysis_window(self):
        patient_id =  int(self.listWidget.currentItem().text().split(' ')[0])
        analysis_window = AnalysisWindow(patient_id)
        self.child_windows.append(analysis_window)
        analysis_window.show()








    '''def get_graphs(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);")
        if not fileName:
            print('Error')
            return

        get_diagrams(fileName)

    def input_form_window(self):
        input_win = ParameterInputWindow()
        self.child_windows.append(input_win)
        input_win.show()'''