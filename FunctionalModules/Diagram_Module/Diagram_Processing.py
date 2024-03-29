from PyQt5.QtWidgets import QMessageBox

from FunctionalModules.DB_Module.db_module import *
from utilits import *
from FunctionalModules.Diagram_Module.diagrams import *
from FunctionalModules.Diagram_Module.manual_prediction import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Models.ModelFactory import *
from Models.Patient import Patient

# пациент [ID, имя, фамилия, отчество, дата рождения, диаг, диаг2, гены, пол, возраст]
# анализ [ID, ID_пациента, дата]
# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]
# datetime.date(1957, 1, 1)


class PatientDataProcessor:
    def __init__(self):
        self.catalog = MainDBController.GetAllParameterCatalog()
        self.prepared_data = {}

    def fill_patients(self, ids: list):
        #patients=  MainDBController.GetAllPatients()
        for pat_id in ids:
            pat = MainDBController.GetPatientByID(pat_id)[0]
            if len(pat)==0:
                continue
            analysis_dct = self.prepared_data[f"{pat[2]} {pat[1]} {pat[3]}"] = {}
            #self.fill_patient_with_dates(analysis_dct, pat[0])
            return analysis_dct


    def fill_patient_with_dates(self, dct, patient_id:int, dates:list):
        #dates = MainDBController.GetAllAnalysisByPatientID(patient_id)
        for date in dates:
            analysis_by_date = MainDBController.GetAllAnalysisByPatinetIDandDate(patient_id, str(date))[0]

            current_patient = MainDBController.GetPatientByID(patient_id)[0]
            patient_diagnosis = current_patient[6]
            patient_birthday = current_patient[4]
            age_on_date = int((date - patient_birthday).days/365)

            param_dct = dct[str(analysis_by_date[2])] = {}
            param_dct['Возраст'] = age_on_date
            param_dct['Диагноз'] = patient_diagnosis
            isValid = self.fill_analysis_with_parameters(param_dct, analysis_by_date[0])

    def fill_analysis_with_parameters(self, dct, analysis_id):
        params = MainDBController.GetAllParametersByAnalysisID(analysis_id)
        if(len(params) ==0):
            return False
        for param in params:
            param_name = self.catalog[param[1]-1][1]
            dct[param_name]= {}
            dct[param_name]['Результат'] = param[2]
        return True

class DiagnosisProcessor:
    def __init__(self):
        self.data_processor = PatientDataProcessor()

    def GetDiagnosis(self, patient_id:int, analysis_date:datetime, xlsx_path):
        analysis_dct = self.data_processor.fill_patients([patient_id])
        self.data_processor.fill_patient_with_dates(analysis_dct,patient_id, [analysis_date])
        diagnosis = predict_by_xlsx(xlsx_path,self.data_processor.prepared_data)
        return diagnosis


class DiagramProcessor:
    def MakeRadar(self, patient:Patient, analysis_date:datetime):
        try:
            t, b = make_radars_from_dic(patient.to_json(analysis_date))
        except Exception:
            print('Невозможно построить график по данным анализам')
            return
        t_canvas = MplCanvas(fig=t)
        b_canvas = MplCanvas(fig=b)
        return t_canvas, b_canvas

    def MakeTimeDiagram(self, patient:Patient, start_date:datetime, end_date:datetime):
        try:
            t,b = make_time_diagrams_from_dic(patient.to_json(start_date,end_date))
        except Exception:
            print('Невозможно построить график по данным анализам')
            return
        t_canvas = MplCanvas(fig=t)
        b_canvas = MplCanvas(fig=b)
        return t_canvas, b_canvas

    def MakeTriangleDiagram(self, patient:Patient, analysis_date:datetime):
        try:
            f = make_triangle_radar_from_dic(patient.to_json(analysis_date))
        except Exception:
            print('Невозможно построить график по данным анализам')
            return
        f_canvas = MplCanvas(fig=f)
        return f_canvas




    def _GetJsonByPatient(self, patient_id:int):
        """Устарел. Не испльзуй"""
        self.data_processor = PatientDataProcessor()
        analysis_dct = self.data_processor.fill_patients([patient_id])
        dates = MainDBController.GetAllAnalysisByPatientID(patient_id)
        dates = [date[2] for date in dates]
        self.data_processor.fill_patient_with_dates(analysis_dct,patient_id, dates)
        print(self.data_processor.prepared_data)
        return self.data_processor.prepared_data

    def _save_to_json(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.data_processor.prepared_data))



class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=1, height=1, dpi=100, fig=None):
        if fig is None:
            return
        self.Figure = fig
        super(MplCanvas, self).__init__(fig)

