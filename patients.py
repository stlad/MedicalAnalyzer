import json

class Analysis:
    def __init__(self, name='', surname = '', patron = '', id=1):
        self.name =name
        self.id = id
        self.surname =surname
        self.patronymic =patron
        self.main_parameters = {}
        self.cytokine_status = {}
        self._set_empty_main_params()
        self._set_empty_cytocine_params()


    def _set_empty_main_params(self):
        self.main_parameters = {}
        self.main_parameters['Нейтрофилы (NEU)'] = self._get_template_line()
        self.main_parameters['Лимфоциты (LYMF)'] = self._get_template_line()
        self.main_parameters['Общие T-лимфоциты (CD45+CD3+)'] = self._get_template_line()
        self.main_parameters['Т-хелперы (CD45+CD3+CD4+)'] = self._get_template_line()
        self.main_parameters['Т-цитотоксические лимфоциты (CD45+CD3+СD8+)'] = self._get_template_line()
        self.main_parameters['Общие В-лимфоциты (CD45+CD19+)'] = self._get_template_line()


    def _set_empty_cytocine_params(self):
        pass

    def _get_template_line(self, param_name=''):
        return {
            'Отклонение': '',
            'Результат': 0,
            'Ед.изм.': '10Е9/л',
            'Реф.интервал от': 0,
            'Реф.интервал до': 0
        }

    def save_patient_to_DB(self):
        PersonalDB.append(self)

    def _get_all_params_in_dct(self):
        return {'id':self.id,
                'Имя': self.name,
                'Фамилия': self.surname,
                'Отчество':self.patronymic,
                **self.main_parameters,
                **self.cytokine_status}

    def serialyze_to_json(self, filename):
        with open(filename+'.json', 'w') as outfile:
            json.dump(self._get_all_params_in_dct(), outfile)

def get_BLACK_ANALYSIS():
    return Analysis()

def get_TEST_ANALYSIS():
    p = Analysis()
    p.id = 0
    p.name = 'Иван'
    p.surname = 'Иванов'
    p.patronymic = 'Иванович'
    p.main_parameters['Нейтрофилы (NEU)']['Результат'] = 69.70
    p.main_parameters['Нейтрофилы (NEU)']['Реф.интервал от'] = 40
    p.main_parameters['Нейтрофилы (NEU)']['Реф.интервал до'] = 70
    p.main_parameters['Нейтрофилы (NEU)']['Отклонение'] = '<'
    return p

def load_Patient_from_Json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    patient = Analysis()
    patient.id = data['id']
    patient.name = data['Имя']
    patient.surname = data['Фамилия']
    patient.patronymic = data['Отчество']

    for index, key in enumerate(data):
        if index >=4 and index <=9:
            patient.main_parameters[key] = data[key]
    return patient


#p = get_TEST_PATIENT()
PersonalDB = [get_BLACK_ANALYSIS(), get_TEST_ANALYSIS()]


