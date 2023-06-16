import datetime

from Models.Analysis import Analysis
from Models.Patient import Patient
from Models.Parameters import Parameter

from FunctionalModules.DB_Module.db_module import *

def CreateFullPatientFromDB(pat_id:int):
    '''Осуществляет обращение к БД. Создает экземпляр пациента, полностью заполненного всеми анализами'''
    catalog = MainDBController.GetAllParameterCatalog()
    patient = Patient(MainDBController.GetPatientByID(pat_id)[0])
    for anal_list in MainDBController.GetAllAnalysisByPatientID(pat_id):
        current_anal = Analysis(patient, anal_list)
        params_list = MainDBController.GetAllParametersByAnalysisID(current_anal.id)
        for i in range(len(catalog)):
            if params_list[0] == params_list[1] and params_list[2] == params_list[3] and params_list[4] == params_list[5]:
                param = Parameter(current_anal, params_list[i*2], catalog[i])
            else:
                param = Parameter(current_anal, params_list[i], catalog[i])
    return patient

def PackOneAnalysisByLists(pat:list, anal:list, params:list, full_catalog:list):
    '''Создает экземпляр АНАЛИЗА с пиркрепленным пациентом. Используются листы значений из БД. Обращения к базе данных нет'''
    patient = Patient(pat)
    anaysis = Analysis(patient, anal)
    for i in range(len(params)):
        param = Parameter(anaysis, params[i], full_catalog[i])
    return anaysis
