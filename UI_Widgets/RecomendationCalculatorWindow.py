from  PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QMessageBox


class RecomendationCalculatorWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        loadUi('UIs\RecomendationCalculatorWindow.ui',self)
        self._parent_main_window = parent_window
        self.setWindowTitle('Калькулятор рекомендаций')

        self._init_UI()

    def _init_UI(self):
        self.addLineBtn.clicked.connect(lambda: self._add_row())
        self.removeLineBtn.clicked.connect(lambda: self._remove_row())


    def _add_row(self):
        row_cnt = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_cnt)




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

