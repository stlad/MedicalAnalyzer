import os
from PyQt5.QtWidgets import *
from  PyQt5.uic import loadUi
from DB_Module.db_module import *
from  UI_Widgets.CreatePatient_window import *
from PyQt5.QtCore import Qt
from utilits import *
from SeasonAnalytics_Module.season_analytics import SeasonAnalyzer
from Diagram_Module.Diagram_Processing import MplCanvas
from Diagram_Module.diagrams import MakeSeasonDiagrams
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class SeasonWindow(QWidget):
    def __init__(self, parent_window, s_anal: SeasonAnalyzer):
        super().__init__()
        self.SeasonAnalyzer = s_anal
        self.catalog = MainDBController.GetAllParameterCatalog()
        self.initUI()

    def initUI(self):
        loadUi('UIs\SeasonWindow.ui', self)
        self.child_windows = []

        self.save_btn.clicked.connect(lambda : self._save_analyzer_to_xlsx())
        self.draw_btn.clicked.connect(lambda :self.draw_graphs())
        self._fill_catalog_box()
        self.name_edit.setText(self.SeasonAnalyzer.main_df['Пациент'].iloc[0])

    def _fill_catalog_box(self):
        for param in self.catalog:
            self.catalog_box.addItem(param[1])

    def _save_analyzer_to_xlsx(self):
        name, type = QFileDialog.getSaveFileName(self, 'Save File', '', '(*.xlsx)')
        if name == '':
            return

        self.SeasonAnalyzer.write_xlsx(name)


    def draw_graphs(self):
        for row in range(self.graph_layout.rowCount()):
            for col in range(self.graph_layout.columnCount()):
                w = self.graph_layout.itemAtPosition(row, col)
                if w is not None:
                    if 'Figure' in list(w.widget().__dict__.keys()):
                        fig = w.widget().Figure.clf()
                        #plt.close() # можно убрать (если рисуются окошки)
                    w.widget().deleteLater()

        catalog_index = self.catalog_box.currentIndex()
        catalog_data = self.catalog[catalog_index]

        automn_data = self.SeasonAnalyzer.au_df[['Дата',catalog_data[1]]]
        spring_data = self.SeasonAnalyzer.sp_df[['Дата',catalog_data[1]]]
        rmin = catalog_data[3]
        rmax = catalog_data[4]

        automn_canvas = MplCanvas(fig = MakeSeasonDiagrams(automn_data, rmin, rmax, 1))
        spring_canvas =MplCanvas(fig = MakeSeasonDiagrams(spring_data, rmin, rmax, 0))

        toolbar = NavigationToolbar2QT(automn_canvas, self)
        self.graph_layout.addWidget(toolbar, 0, 0)
        self.graph_layout.addWidget(automn_canvas, 1, 0)

        toolbar1 = NavigationToolbar2QT(spring_canvas, self)
        self.graph_layout.addWidget(toolbar1, 2, 0)
        self.graph_layout.addWidget(spring_canvas, 3, 0)
