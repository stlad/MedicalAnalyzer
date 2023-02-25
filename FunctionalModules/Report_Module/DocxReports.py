from docx import Document
from copy import deepcopy
from FunctionalModules.DB_Module.db_module import *
from utilits import  date_sql_to_text_format
from Models.Patient import Patient
from Models.Analysis import Analysis


class DocxReporter():

    def __init__(self, analysis:Analysis):
        self.patient = analysis.patient
        self.analysis = analysis

        self.doc = self._get_classic_table()



        pass

    def _get_table_from_template(self):
        doc = Document('form_template')
        return deepcopy(doc.tables[0])


    def _get_classic_table(self):
        template_table = self._get_table_from_template()
        doc = Document()
        paragraph = doc.add_paragraph()
        paragraph._p.addnext(template_table._tbl)

        tbl = doc.tables[0]

        tbl.rows[0].cells[1].text = f"{self.patient.surname} {self.patient.name} {self.patient.patronymic} "
        tbl.rows[1].cells[1].text = self.patient.gender # ПОЛ
        tbl.rows[2].cells[1].text = date_sql_to_text_format(str(self.analysis.analysis_date)) # ДАТА АНАЛИЗА
        tbl.rows[3].cells[1].text = self.patient.get_age_by_date(self.analysis.analysis_date) + ' Полных лет'# ВОЗРАСТ
        tbl.rows[4].cells[1].text = self.patient.diag # ДИАГНОЗ 1
        tbl.rows[5].cells[1].text = self.patient.second_diag # ДИАГНОЗ 2

        tbl.rows[6].cells[1].text = self.patient.genes  # ГЕНЫ 1,2,3
        tbl.rows[7].cells[1].text = self.patient.genes  # ГЕНЫ 1,2,3
        tbl.rows[8].cells[1].text = self.patient.genes  # ГЕНЫ 1,2,3

        tbl.rows[9].cells[1].text = '0' if self.analysis.analysis_date.month in [3,4,5,6,7,8] else '1'



    def _fill_params(self, tbl):
        i = 0


    def save_to_file(self, filename):
        if self.doc == None:
            return
        self.doc.save(filename)



'''pat = MainDBController.GetAllPatients()[0]
anal = MainDBController.GetAllAnalysisByPatientID(5)[0]
print(pat)
print(str(anal[2]))
print(pat[4])
PrintedForm(pat,anal)'''


# пациент [ID, имя, фамилия, отчество, дата рождения, диаг, диаг2, гены, пол, возраст]
# анализ [ID, ID_пациента, дата]
# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]

p = Patient(MainDBController.GetPatientByID(5)[0])
a = Analysis(p, MainDBController.GetAllAnalysisByPatientID(5)[0])

form = DocxReporter(p, a)
form.save_to_file('hello.docx')
print(1)
#p = Patient(MainDBController.GetAllPatients()[0])
#r = p.to_DB_list()
#print(1)
