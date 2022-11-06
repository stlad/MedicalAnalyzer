from DB_Module.db_module import *
import datetime, json
from utilits import *
from Diagram_Module.diagrams import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy



# пациент [ID, имя, фамилия, отчество, дата, рождения, диаг, диаг2, гены, пол, возраст]
# анализ [ID, ID_пациента, дата]
# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]
# datetime.date(1957, 1, 1)

class DiagramProcessor:
    def __init__(self):
        self.prepared_data = {}
        self.catalog = MainDBController.GetAllParameterCatalog()

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


    def MakeRadar(self, patient_id:int, analysis_date:datetime):
        analysis_dct = self.fill_patients([patient_id])
        self.fill_patient_with_dates(analysis_dct,patient_id, [analysis_date])
        try:
            t,b = make_radars_from_dic(self.prepared_data)
        except KeyError:
            print('Не заполнены анализы')
            return
        t_canvas = MplCanvas(fig=t)
        b_canvas = MplCanvas(fig=b)
        return t_canvas, b_canvas

    def MakeTimeDiagram(self, patient_id:int, start_date:datetime, end_date:datetime):
        analysis_dct = self.fill_patients([patient_id])
        dates = MainDBController.GetAllAnalysisBetweenDates(patient_id,start_date,end_date)
        dates = [date[2] for date in dates]
        self.fill_patient_with_dates(analysis_dct,patient_id, dates)
        try:
            t,b = make_time_diagrams_from_dic(self.prepared_data)
        except KeyError:
            print('Не заполнены анализы')
            return
        t_canvas = MplCanvas(fig=t)
        b_canvas = MplCanvas(fig=b)
        return t_canvas, b_canvas


    def GetJsonByPatient(self, patient_id:int):
        analysis_dct = self.fill_patients([patient_id])
        dates = MainDBController.GetAllAnalysisByPatientID(patient_id)
        dates = [date[2] for date in dates]
        self.fill_patient_with_dates(analysis_dct,patient_id, dates)
        print(self.prepared_data)
        return self.prepared_data

    def _save_to_json(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.prepared_data))


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=1, height=1, dpi=100, fig=None):
        if fig is None:
            return
        super(MplCanvas, self).__init__(fig)

'''d = DiagramProcessor()

d.GetJsonByPatient(5)
d._save_to_json('analysis.json')'''
#print(list(d.prepared_data.keys()))
#cat = MainDBController.GetAllParameterCatalog()
#for index, param in enumerate(cat):
#    print(index, param)

#3 2 8 10 12 9
