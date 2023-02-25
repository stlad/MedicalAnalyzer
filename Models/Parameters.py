from Analysis import Analysis
from Patient import Patient
from FunctionalModules.DB_Module.db_module import *

# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]


class Parameter():

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

        self.own_analysis.add_parameter(self)




