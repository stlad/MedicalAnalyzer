import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *
from UI_Widgets.Analysis_Window import *
from Diagram_Module.Diagram_Processing import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib import pyplot as plt

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

        self.diagram_processor = DiagramProcessor()

        self.refresh_all_lists()
        self.patient_create_btn.clicked.connect(lambda :self.open_patient_creation())
        self.patient_delete_btn.clicked.connect(lambda: self.delete_chosen_patient())
        self.patient_select_btn.clicked.connect(lambda: self.get_selected_patient_id())
        self.patients_list.currentItemChanged.connect(lambda : (self.get_selected_patient_id()))
        self.analysis_create_btn.clicked.connect(lambda :self.create_analysis())
        self.analysis_list.currentItemChanged.connect(lambda: (self.get_selected_analysis_id()))
        self.analysis_delete_btn.clicked.connect(lambda :self.delete_chosen_analysis())
        self.analisys_select_btn.clicked.connect(lambda:self.open_analysis_creation())
        self.tb_graph_btn.clicked.connect(lambda:self.create_radars())
        self.comboBox.currentIndexChanged.connect(lambda: self.graph_preparation())
        self.diagnosis_btn.clicked.connect(lambda:self.get_diagnosis())


        self.toolBox.setItemText(0, 'Пациенты')
        self.toolBox.setItemText(1, 'Анализы и графики')
        self.toolBox.setItemText(2, 'Диагнозы')

        self.show()

    def get_diagnosis(self):
        proc = DiagnosisProcessor()
        diag = proc.GetDiagnosis()
        # СДЕЛАТЬ ОБНОВЛЕНИЕ ДИАГНОЗА В БД
        # СДЕЛАТЬ ВЫВОД в #self.diagnosis_edit().

    def graph_preparation(self):
        if self.comboBox.currentIndex()==0:
            self.graph_start_edit.setEnabled(False)
            self.graph_end_edit.setEnabled(False)
        else:
            self.graph_start_edit.setEnabled(True)
            self.graph_end_edit.setEnabled(True)


    def refresh_all_lists(self):
        self.refresh_patients_list()
        self.refresh_analysis_list()

    def refresh_patients_list(self):
        """Заполнит таблицу пациентов и вернет их полный список"""
        self.patients_list.clear()
        patients = MainDBController.GetAllPatients()
        self.patients = []
        for pat in patients:
            self.patients.append(pat)
            line = f'{pat[2]} {pat[1]} {pat[3]} {date_sql_to_text_format(str(pat[4]))} |{pat[0]}'
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
            line = date_sql_to_text_format(str(an[2]))
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

    def update_patients_toolbox_name(self):
        self.toolBox.setItemText(0,self.patients_list.currentItem().text())

    def update_analysis_toolbox_name(self):
        self.toolBox.setItemText(1,self.analysis_list.currentItem().text())

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
        a_date = date_to_sql_format(a_date)
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


    def create_radars(self):
        #for i in reversed(range(self.graph_layout.count())):
        #    self.graph_layout.itemAt(i).widget().deleteLater()

        for row in range(self.graph_layout.rowCount()):
            for col in range(self.graph_layout.columnCount()):
                w = self.graph_layout.itemAtPosition(row, col)
                if w is not None:
                    #plt.close(w.widget().Figure)
                    w.widget().deleteLater()

        pat_id = self.current_patient_id
        index = self.analysis_list.currentRow()

        if self.comboBox.currentIndex() == 0:
            if index ==-1:
                return
            current_anal_date = self.analysis[index][2]
            figs = self.diagram_processor.MakeRadar(pat_id, current_anal_date)
            try:
                toolbar = NavigationToolbar2QT(figs[0],self)
                self.graph_layout.addWidget(toolbar, 1, 0)
                self.graph_layout.addWidget(figs[0], 0, 0)

                toolbar1 = NavigationToolbar2QT(figs[1], self)
                self.graph_layout.addWidget(toolbar1, 1, 1)
                self.graph_layout.addWidget(figs[1], 0, 1)
            except TypeError:
                print('невозможно построить графики')
        else:
            start_date =str_to_date(self.graph_start_edit.text())
            end_date =str_to_date(self.graph_end_edit.text())
            figs = self.diagram_processor.MakeTimeDiagram(pat_id, start_date,end_date)
            try:
                toolbar = NavigationToolbar2QT(figs[0],self)
                self.graph_layout.addWidget(toolbar, 0, 0)
                self.graph_layout.addWidget(figs[0], 1, 0)

                toolbar1 = NavigationToolbar2QT(figs[1], self)
                self.graph_layout.addWidget(toolbar1, 2, 0)
                self.graph_layout.addWidget(figs[1], 3, 0)
            except TypeError:
                print('невозможно построить графики')
