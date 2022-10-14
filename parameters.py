import json




class Patient:
    def __init__(self, name='', surname = '', patron = ''):
        self.name =name
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
        return {'Имя': self.name,
                'Фамилия': self.surname,
                'Отчество':self.patronymic,
                **self.main_parameters,
                **self.cytokine_status}
    def serialyze_to_json(self):
        with open(f'{self.surname} {self.name}.json', 'w') as outfile:
            json.dump(self._get_all_params_in_dct(), outfile)

def get_BLANK_PATIENT():
    return Patient()
def get_TEST_PATIENT():
    p = Patient()
    p.name = 'Иван'
    p.surname = 'Иванов'
    p.patronymic = 'Иванович'
    p.main_parameters['Нейтрофилы (NEU)']['Результат'] = 69.70
    p.main_parameters['Нейтрофилы (NEU)']['Реф.интервал от'] = 40
    p.main_parameters['Нейтрофилы (NEU)']['Реф.интервал до'] = 70
    p.main_parameters['Нейтрофилы (NEU)']['Отклонение'] = '<'
    return p

#p = get_TEST_PATIENT()
PersonalDB = [get_BLANK_PATIENT(), get_TEST_PATIENT()]