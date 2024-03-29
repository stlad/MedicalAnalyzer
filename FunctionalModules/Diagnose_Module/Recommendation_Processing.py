import os

from FunctionalModules.Diagram_Module.diagrams import *
from FunctionalModules.Diagram_Module.manual_prediction import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Models.ModelFactory import *
from Models.Patient import Patient
from FunctionalModules.Diagnose_Module.diagnoses import check_statuses, check_diagnoses
from FunctionalModules.DB_Module.db_module import *


class RecommendationProcessor():
    def __init__(self):
        return

    def MakeRecommendation(self, patient:Patient, analisys_date:datetime):
        try:
            #recommend = check_statuses(patient.to_json(analisys_date))
            #recommend = check_base_diagnoses('FunctionalModules/Diagnose_Module/recomendations.xlsx', patient.to_json(analisys_date))
            recommend = check_diagnoses(MainDBController.GetAllCalcRules() ,patient.to_json(analisys_date))
            return recommend
        except KeyError:
            print("Не заполнены анализы")
            return ""


    def _fake_recommendation(self, pat_json):
        return "РЕКОМЕНДАЦИЯ"