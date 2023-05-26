from  PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QMessageBox
from FunctionalModules.DB_Module.db_module import *

class RecomendationCalculatorWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        loadUi('UIs\RecomendationCalculatorWindow.ui',self)
        self._parent_main_window = parent_window
        self.setWindowTitle('Калькулятор рекомендаций')
        self.rules = []
        self._init_UI()

    def _init_UI(self):
        self.addLineBtn.clicked.connect(lambda: self._add_row())
        self.removeLineBtn.clicked.connect(lambda: self._remove_row())
        self.db_save_btn.clicked.connect(lambda: self._save_to_db())
        self.add_minus_btn.clicked.connect(lambda : self._add_to_current_cell("[[-]]"))
        self.add_plus_btn.clicked.connect(lambda : self._add_to_current_cell("[[+]]"))
        self._refresh_rules()


    def _add_to_current_cell(self,item):
        self.tableWidget.currentItem().setText(self.tableWidget.currentItem().text()+item)

    def _load_table(self):
        tb = self.tableWidget
        for row, rule in enumerate(self.rules):
            if tb.rowCount() <= row:
                tb.insertRow(tb.rowCount())
            tb.setItem(row,0, QTableWidgetItem(rule.expression))
            tb.setItem(row,1, QTableWidgetItem(rule.cause))
            tb.setItem(row,2, QTableWidgetItem(rule.recommendation))
            tb.setItem(row,3, QTableWidgetItem(rule.variable))
            tb.setItem(row,4, QTableWidgetItem(rule.value))
            tb.setItem(row,5, QTableWidgetItem(str(rule.for_autumn)))
            tb.setItem(row,6, QTableWidgetItem(str(rule.for_spring)))


    def _save_to_db(self):
        for row, rule in enumerate(self.rules):
            rule.expression = self.tableWidget.item(row, 0).text()
            rule.cause = self.tableWidget.item(row, 1).text()
            rule.recommendation = self.tableWidget.item(row, 2).text()
            rule.variable = self.tableWidget.item(row, 3).text()
            rule.value = self.tableWidget.item(row, 4).text()
            rule.for_autumn = bool(self.tableWidget.item(row, 5).text())
            rule.for_spring = bool(self.tableWidget.item(row, 6).text())

            if rule.db_id==0:
                MainDBController.SaveCalcRule(rule)
            else:
                MainDBController.UpdateCalcRule(rule)
        self._refresh_rules()

    def _add_row(self):
        row_cnt = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_cnt)
        for i in range(7):
            self.tableWidget.setItem(row_cnt, i, QTableWidgetItem(""))
        self.rules.append(CalculatorRule())


    def _refresh_rules(self):
        self.rules = MainDBController.GetAllCalcRules()
        self._load_table()


    def _remove_row(self):
        row = self.tableWidget.currentRow()
        if row==-1:
            return

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удаление условия")
        dlg.setText(f"Удалить строку: {row+1}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            self.tableWidget.removeRow(row)
            MainDBController.DeleteRule(self.rules[row])

