import FunctionalModules.DB_Module.db_module
from FunctionalModules.Diagnose_Module.Recommendation_Processing import RecommendationProcessor
from  UI_Widgets.CreatePatient_window import *
from UI_Widgets.Analysis_Window import *
from UI_Widgets.RecomendationCalculatorWindow import *
from FunctionalModules.Diagram_Module.Diagram_Processing import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib import pyplot as plt
from UI_Widgets.Season_window import SeasonWindow
from FunctionalModules.SeasonAnalytics_Module.season_analytics import SeasonAnalyzer
from Models.ModelFactory import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi('UIs\MainWindow.ui', self)
        self.setWindowTitle('Medical Analyzer')
        self.child_windows = []

        self.patients = []
        self.current_patient_id = 0
        self.current_analysis_id = 0
        self.current_analysis_date = ''
        self.analysis = []

        self.diagram_processor = DiagramProcessor()

        self.refresh_all_lists()
        self.patient_create_btn.clicked.connect(lambda :self.open_patient_creation())
        self.patient_delete_btn.clicked.connect(lambda: self.delete_chosen_patient())

        self.patient_select_btn.clicked.connect(lambda: self.open_season_analyzer())

        self.patients_list.currentItemChanged.connect(lambda : (self.get_selected_patient_id()))
        self.patients_list.currentItemChanged.connect(lambda: self.update_toolbox_pat_name())

        self.analysis_create_btn.clicked.connect(lambda :self.create_analysis())
        self.analysis_list.currentItemChanged.connect(lambda: (self.get_selected_analysis_id()))
        self.analysis_list.currentItemChanged.connect(lambda: self.update_toolbox_analysis_name())

        self.analysis_delete_btn.clicked.connect(lambda :self.delete_chosen_analysis())
        self.analisys_select_btn.clicked.connect(lambda:self.open_analysis_creation())
        self.tb_graph_btn.clicked.connect(lambda:self.create_radars())
        self.comboBox.currentIndexChanged.connect(lambda: self.graph_preparation())
        self.diagnosis_btn.clicked.connect(lambda:self.get_diagnosis())
        self.load_from_file_btn.clicked.connect(lambda :self.load_from_file())


        self.toolBox.setItemText(0, 'Пациенты')
        self.toolBox.setItemText(1, 'Анализы и графики')
        self.toolBox.setItemText(2, 'Рекомендации')

        #self.actionOpenCalculator.triggered.connect(lambda: print("нажато"))
        self._create_menubar()

        self.show()

    def _create_menubar(self):
        menubar = self.menubar
        recMenu = menubar.addMenu('Меню')
        createCalcAction = QAction(self)
        menubar.addMenu
        createCalcAction.setText("Калькулятор рекомендаций")
        createCalcAction.triggered.connect(lambda: self._open_new_window(RecomendationCalculatorWindow(self)))
        recMenu.addAction(createCalcAction)

    def _open_new_window(self, window):
        self.child_windows.append(window)
        window.show()


    def open_season_analyzer(self):
        print(self.current_patient_id)
        if self.current_patient_id <=0:
            return
        s_analyzer = SeasonAnalyzer(self.current_patient_id)
        if s_analyzer.main_df.empty:
            return
        season_window = SeasonWindow(self, s_analyzer)
        self.child_windows.append(season_window)
        season_window.show()

    def update_toolbox_pat_name(self):
        index = self.patients_list.currentRow()
        if index < 0:
            self.toolBox.setItemText(0, 'Пациенты')
            return
        pat = [p for p in self.patients if p[0]==self.current_patient_id][0]
        name, sur, patr = pat[1], pat[2], pat[3]
        self.toolBox.setItemText(0, f'{sur} {name} {patr}') #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ

    def update_toolbox_analysis_name(self):
        index = self.analysis_list.currentRow()
        if index < 0:
            self.toolBox.setItemText(1, 'Анализы')
            return
        analysis = [a for a in self.analysis if a[0]==self.current_analysis_id][0]
        self.toolBox.setItemText(1, f'{str(analysis[2])}')

    def load_from_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', filter="(*.json)")
        if fname[0]=='':
            return
        FunctionalModules.DB_Module.db_module.load_data_from_json(filename=fname[0])


    def get_diagnosis(self):
        proc = RecommendationProcessor()
        # СДЕЛАТЬ ОБНОВЛЕНИЕ ДИАГНОЗА В БД
        pat_id = self.get_selected_patient_id()
        current_anal_date = self.current_analysis_date
        try:
            diag = proc.MakeRecommendation(CreateFullPatientFromDB(pat_id), current_anal_date)
        except Exception as e :
            #diag = e.args[0]
            diag = 'Параметры не соответствуют ни одному из условий для рекомендаций.'
        self.diagnosis_edit.setText(diag)

    def graph_preparation(self):
        if self.comboBox.currentIndex()==1:
            self.graph_start_edit.setEnabled(True)
            self.graph_end_edit.setEnabled(True)
        else:
            self.graph_start_edit.setEnabled(False)
            self.graph_end_edit.setEnabled(False)


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
            line = f'{pat[2]} {pat[1]} {pat[3]}   {date_sql_to_text_format(str(pat[4]))} '# |{pat[0]}' #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
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
        #print(index, current_patient)
        #print(current_patient[0])
        self.current_patient_id = current_patient[0]
        self.refresh_analysis_list()
        return self.current_patient_id

    def get_selected_analysis_id(self):
        index = self.analysis_list.currentRow()
        current_anal = self.analysis[index]
        self.current_analysis_id = current_anal[0]
        if index != -1:
            self.current_analysis_date = current_anal[2]
        else:
            current_anal = None


    def update_patients_toolbox_name(self):
        self.toolBox.setItemText(0,self.patients_list.currentItem().text())

    def update_analysis_toolbox_name(self):
        self.toolBox.setItemText(1,self.analysis_list.currentItem().text())



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


    def _clear_graphs(self):
        for row in range(self.graph_layout.rowCount()):
            for col in range(self.graph_layout.columnCount()):
                w = self.graph_layout.itemAtPosition(row, col)
                if w is not None:
                    if 'Figure' in list(w.widget().__dict__.keys()):
                        #plt.close(w.widget().Figure)
                        #plt.figure().close('all')
                        fig = w.widget().Figure.clf()
                        plt.close() # можно убрать (если рисуются окошки)
                    w.widget().deleteLater()

    def create_radars(self):
        self._clear_graphs()
        pat_id = self.current_patient_id
        index = self.analysis_list.currentRow()

        current_patient = CreateFullPatientFromDB(pat_id)
        if self.comboBox.currentIndex() == 0:
            if index ==-1:
                return
            current_anal_date = self.analysis[index][2]
            self._draw_radars(current_patient, current_anal_date)

        elif self.comboBox.currentIndex() == 2:
            if index ==-1:
                return
            current_anal_date = self.analysis[index][2]
            self._draw_triangle_diagramms(current_patient, current_anal_date)
        else:
            self._draw_time_diagrams(current_patient)


    def _draw_radars(self, patient, current_anal_date):
        figs = self.diagram_processor.MakeRadar(patient, current_anal_date)
        try:
            toolbar = NavigationToolbar2QT(figs[0], self)
            self.graph_layout.addWidget(toolbar, 1, 0)
            self.graph_layout.addWidget(figs[0], 0, 0)

            toolbar1 = NavigationToolbar2QT(figs[1], self)
            self.graph_layout.addWidget(toolbar1, 1, 1)
            self.graph_layout.addWidget(figs[1], 0, 1)
        except Exception:
            #print('невозможно построить графики')
            QMessageBox.about(self, "Ошибка в построении графиков", "Невозможно построить график по данным анализам")


    def _draw_time_diagrams(self, patient):
        start_date = str_to_date(self.graph_start_edit.text())
        end_date = str_to_date(self.graph_end_edit.text())
        figs = self.diagram_processor.MakeTimeDiagram(patient, start_date, end_date)
        try:
            toolbar = NavigationToolbar2QT(figs[0], self)
            self.graph_layout.addWidget(toolbar, 0, 0)
            self.graph_layout.addWidget(figs[0], 1, 0)

            toolbar1 = NavigationToolbar2QT(figs[1], self)
            self.graph_layout.addWidget(toolbar1, 2, 0)
            self.graph_layout.addWidget(figs[1], 3, 0)
        except Exception:
            QMessageBox.about(self, "Ошибка в построении графика", "Невозможно построить график по данным анализам")

    def _draw_triangle_diagramms(self, patient, current_anal_date):
        fig = self.diagram_processor.MakeTriangleDiagram(patient, current_anal_date)
        try:
            toolbar = NavigationToolbar2QT(fig, self)
            self.graph_layout.addWidget(toolbar, 1, 0)
            self.graph_layout.addWidget(fig, 0, 0)
        except Exception:
            QMessageBox.about(self, "Ошибка в построении графика", "Невозможно построить график по данным анализам")

