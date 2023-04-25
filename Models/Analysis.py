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
        self.season = '0' if self.analysis_date.month in [3,4,5,6,7,8] else '1'

        if self.patient is None:
            return
        self.patient.add_analysis(self)

    def to_DB_list(self):
        return self._original_data

    def add_parameter(self, param):
        self.parameters.append(param)

    def to_json(self):
        res = {}
        res['Возраст'] = self.patient.get_age_by_date(self.analysis_date)
        res['Диагноз'] = self.patient.diag
        for param in self.parameters:
            res[param.name] = param.to_json()
        return res

    def __str__(self):
        return str(self.analysis_date)

