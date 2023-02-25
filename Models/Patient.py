# пациент [ID, имя, фамилия, отчество, дата рождения, диаг, диаг2, гены, пол, возраст]

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
        return str(int((d - self.birthdate).days/ 365))

    def add_analysis(self, a):
        self.analysis.append(a)

