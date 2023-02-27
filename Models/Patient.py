# пациент [ID, имя, фамилия, отчество, дата рождения, диаг, диаг2, гены, пол, возраст]
import datetime

class Patient:
    '''Представляет собой пациента. Предпочтительно использовать этот класс'''
    def __init__(self, l):
        self.from_DB_list(l)
        self.analysis = []


    def from_DB_list(self, l):
        self._original_data = l
        self.id = l[0]
        self.name = l[1]
        self.surname = l[2]
        self.patronymic = l[3]
        self.birthdate = l[4]
        self.diag = l[5]
        self.second_diag = l[6]
        self.genes = l[7]
        self.gender = l[8]
        self.age = l[9]

    def to_DB_list(self):
        return self._original_data

    def get_age_by_date(self, d):
        return int((d - self.birthdate).days/ 365)

    def add_analysis(self, a):
        self.analysis.append(a)

    def to_json(self,start_date=None, end_date=None):
        """
        Сериализация в json
        :parameter start_date: Дата анализа, который надо сериализовать. Если указаны оба параметра - дата начала интервала
        :parameter end_date: Дата конца интервала.
        """
        res = {}
        for anal in self.analysis:
            if not self._check_date(anal.analysis_date, start_date, end_date):
                continue
            res[str(anal.analysis_date)] = anal.to_json()
        return {f'{self.surname} {self.name} {self.patronymic}': res}


    def _check_date(self, date, start_interval, end_interval):
        if start_interval is None and end_interval is None:
            return True
        if end_interval is None:
            return date == start_interval
        return date >= start_interval and date <= end_interval

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


