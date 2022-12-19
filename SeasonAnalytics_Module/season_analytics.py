import pandas as pd
from  Diagram_Module.Diagram_Processing import PatientDataProcessor
from DB_Module.db_module import *

catalog = MainDBController.GetAllParameterCatalog()

def get_main_table(patient_id):
    patientProcessor = PatientDataProcessor()
    dates = [d[2] for d in MainDBController.GetAllAnalysisByPatientID(patient_id)]

    analysis_dct = patientProcessor.fill_patients([patient_id])
    patientProcessor.fill_patient_with_dates(analysis_dct, patient_id, dates)
    patient_data = patientProcessor.prepared_data
    name = list(patient_data.keys())[0]
    df = _get_table(name, analysis_dct)

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
        ref_min = param[3]
        ref_max = param[4]
        #df[f'{col_cnt} Отклонение'] = [''] * len(analysis_dct)
        df[f'Отклонение {col_cnt}'] = [_calculate_divation(analysis_dct[i][p]['Результат'], ref_min, ref_max) for i in analysis_dct]
        col_cnt+=1
    return df

def _calculate_divation(val, rmin, rmax):
    if val>=rmax and val <= rmax:
        return 0
    elif val < rmin:
        return val - rmin
    else:
        return val - rmax

def _get_season_by_date(d):
    month =int(d[5:7])
    return 1 if month in [9,10,11,12,1,2] else 0


def _get_season_tables(df):
    autumn_df = df[df['Сезон']==1]
    sprint_df = df[df['Сезон']==0]

    return autumn_df, sprint_df




def _get_avg_param_df(df):
    avg_df = pd.DataFrame()
    avg_df['Сезон'] = ['Осень','Весна']
    cnt=0
    for param in catalog:
        p = param[1]
        au_mean = df[df['Сезон'] == 1][p].mean()
        sp_mean = df[df['Сезон'] == 0][p].mean()
        ref_min = param[3]
        ref_max = param[4]

        avg_df[p] = [au_mean,sp_mean]
        avg_df[f'Отклонение {cnt}'] =[ df[df['Сезон'] == 1][f'Отклонение {cnt}'].mean(),
                                       df[df['Сезон'] == 0][f'Отклонение {cnt}'].mean()]

        cnt+=1
    return avg_df

class SeasonAnalyzer():
    def __init__(self, patient_id):
        self.id = patient_id
        self.main_df = get_main_table(self.id)
        self.au_df, self.sp_df = _get_season_tables(self.main_df)
        self.avg_df = _get_avg_param_df(self.main_df)

    def write_xlsx(self, filename):
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        self.main_df.to_excel(excel_writer=writer, sheet_name='Main')
        self.au_df.to_excel(excel_writer=writer, sheet_name='Осень')
        self.sp_df.to_excel(excel_writer=writer, sheet_name='Весна')
        self.avg_df.to_excel(excel_writer=writer, sheet_name='Среднее')
        writer.close()

#SeasonAnalyzer(5).write_xlsx('out1.xlsx')




'''df = get_main_table(5)
au_df, sp_df = _get_season_tables(df)
avg_df = _get_avg_param_df(df)'''

#write_patient_stats_to_xlsx('out.xlsx', [df, au_df,sp_df,avg_df])
#df = make_season_table(5)
#adf = _get_season_tables(df)
#df.to_excel('out.xlsx', sheet_name='Main')
#write_patient_stats_to_xlsx('out.xlsx', 5)