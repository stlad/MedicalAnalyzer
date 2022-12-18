import pandas as pd
from  Diagram_Module.Diagram_Processing import PatientDataProcessor
from DB_Module.db_module import *

catalog = MainDBController.GetAllParameterCatalog()

def make_season_table(patient_id):
    patientProcessor = PatientDataProcessor()
    dates = [d[2] for d in MainDBController.GetAllAnalysisByPatientID(5)]

    analysis_dct = patientProcessor.fill_patients([patient_id])
    patientProcessor.fill_patient_with_dates(analysis_dct, patient_id, dates)
    patient_data = patientProcessor.prepared_data
    name = list(patient_data.keys())[0]
    df = _get_table(name, analysis_dct)
    print(df)
    return df

def _get_table(name, analysis_dct):
    df = pd.DataFrame()
    df['Пациент'] = [name]*len(analysis_dct)
    df['Дата'] = [d for d in analysis_dct.keys()]
    df[f'Сезон'] = [_get_season_by_date(d) for d in analysis_dct]
    col_cnt=0
    for param in catalog:
        p = param[1]
        df[p] = [analysis_dct[i][p]['Результат'] for i in analysis_dct]
        df[f'{col_cnt} Отклонение'] = [''] * len(analysis_dct)
        col_cnt+=1
    return df

def _get_season_by_date(d):
    month =int(d[5:7])
    return 1 if month in [9,10,11,12,1,2] else 0

df = make_season_table(5)
df.to_excel('out.xlsx')