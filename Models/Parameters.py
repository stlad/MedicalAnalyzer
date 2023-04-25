from Models.Analysis import Analysis


# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]


class Parameter:
    def __init__(self, analysis:Analysis, param:list, catalog_line:list):
        self.from_DB_lists(analysis, param, catalog_line)

    def from_DB_lists(self, analysis: Analysis, param:list, catalog_line:list):
        self.own_analysis = analysis
        self._original_data = param

        self.id =param[0]
        self.catalog_id = param[1]
        self.value = param[2]

        self.name = catalog_line[1]
        self.ref_min = catalog_line[3]
        self.ref_max = catalog_line[4]

        if self.own_analysis is None:
            return
        self.own_analysis.add_parameter(self)


    def to_json(self):
        return {'Результат': self.value}


    def devation_from_interval(self, delta = 0):
        if self.value > self.ref_max + delta:
            return self.value - self.ref_max - delta
        elif self.value < self.ref_min - delta:
            return  self.valuea - self.ref_min - delta
        else:
            return 0


    def __str__(self):
        return f'{self.name}'
