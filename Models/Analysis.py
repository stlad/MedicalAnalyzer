from Models.Patient import Patient

# анализ [ID, ID_пациента, дата]
class Analysis:
    '''Представляет собой класс анализа. Рекомендовано к использованию'''
    def __init__(self, patient: Patient, analysis:list):
        self.patient = patient
        self.from_DB_list(analysis)
        self.parameters = []

    def from_DB_list(self, anal):
        self._original_data = anal
        self.id = anal[0]
        self.analysis_date = anal[2]
        self.patient.add_analysis(self)

    def to_DB_list(self):
        return self._original_data

    def add_parameter(self, param):
        self.parameters.append(param)



