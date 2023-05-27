import psycopg2
from utilits import *
import json
from Models.CalculatorRule import CalculatorRule

class DBController():
    def __init__(self,database = 'MedicalAnalysis_DB', user = 'postgres', password='admin', host='localhost', port='5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        print('User Entered successfully!')

    def _create_connection_to_DB(self):
        '''Создает соединение с базоый данных и возвращает его'''
        try:
            con = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            #print("Database opened successfully!")
            return con
        except psycopg2.OperationalError:
            print('Не получилось подключиться к базе данных')
            return

    def InsertPatient(self, patient_info):
        """Добавить пациента в базу
        :parameter patient_info:
        Список полей пациента формата -
        [фамилия,имя, отчество, день рождения(YYYY-MM-DD), осн диагноз, сопутсв. диагноз, гены, пол]"""
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql=' '.join([f"insert into patients(surname, name,patronymic,birthday,main_diagnosis,concomitant_diagnosis,genes, gender)",
            f"values('{patient_info[0]}','{patient_info[1]}','{patient_info[2]}','{patient_info[3]}', '{patient_info[4]}', '{patient_info[5]}', '{patient_info[6]}', '{patient_info[7]}')"])
        cur.execute(sql)
        con.commit()
        cur.close()

    def DeletePatientById(self, id:int):
        """Удалить пациента из базы по его ID"""
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql = f"delete from patients where patient_id ={id}"
        cur.execute(sql)
        con.commit()
        cur.close()

    def DeleteAnalysisByID(self, id:int):
        """Удалить анализ из базы по его ID"""
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql = f"delete from analysis where analysis_id ={id}"
        cur.execute(sql)
        con.commit()
        cur.close()

    def InsertAnalysis(self, analysis_info):
        """Добавить анализ в базу
        :parameter analysis_info
        Список полей анализа формата -
        [ID пациента, дата анализа(YYYY-MM-DD)]"""
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql=' '.join([f"insert into Analysis(owner_id,analysis_date)",
            f"values({analysis_info[0]},'{analysis_info[1]}')"])
        cur.execute(sql)
        con.commit()
        cur.close()

    def InsertListOfParametersByAnalysisId(self,analysis_id:int, parameters_list:list):
        """Добавить список параметров в БД
        :parameter analysis_id ID анализа
        :parameter parameters_list в формате [[ID параметра из каталога, значение, отклонение],....]
        """
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            for index, param in enumerate(parameters_list):
                sql = f"insert into parameter_results(analysis_id, parameter_id, value, deviation) values({analysis_id}, {param[0]}, {param[1]},'{param[2]}')"
                cur.execute(sql)
                con.commit()

    def UpdateListOfParameters(self, parameters_list):
        """Обновить параметры в БД
        :parameter parameters_list [[parameter_id, new_value]]"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            for index, param in enumerate(parameters_list):
                sql = f"update parameter_results set value={param[1]} where result_id={param[0]}"
                cur.execute(sql)
                con.commit()

    def GetAllParametersByAnalysisID(self, id:int):
        """Получить список всех пациентов в базе"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from parameter_results where analysis_id = {id} order by parameter_id" # ОЧЕНЬ ОПАСНЫЙ МОМЕНТ. ВОЗМОЖНЫ БАГИ ПОСЛЕ ДОБАВЛЕНИЯ СОРТИРОВКИ
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def GetAllPatients(self):
        """Получить список всех пациентов в базе"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select *, age(birthday) as age from patients"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def GetPatientByID(self, id:int):
        """Получить пациента по его ID"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select *, age(birthday) as age from patients where patient_id={id}"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def GetAllAnalysisByPatientID(self,patient_id: int):
        """Получить все анализы одного человека"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from analysis where owner_id = {patient_id} order by analysis_date"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def GetAllAnalysisByPatinetIDandDate(self, patient_id:int, analysis_date):
        """ Получить анализы человека за конкретную дату
        :param patient_id: ID пациента
        :param analysis_date: Дата анализа формата YYYY-MM-DD
        :return:
        """
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from analysis where owner_id = {patient_id} and analysis_date ='{analysis_date}' "
            cur.execute(sql)
            rows = cur.fetchall()
        return rows


    def GetAllParameterCatalog(self):
        """Все параметры из каталога"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from parameter_catalog order by parameter_id"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def GetAllAnalysisBetweenDates(self, patient_id:int, start:datetime, end:datetime):
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from analysis where owner_id = {patient_id} and analysis_date between '{start}' and '{end}'"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def UpdateParameter(self, param_id:int, data:list):
        '''Изменить параметр. Подается ИД, [откл, значенеи]'''
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"update parameters set devation={data[0]}, value={data[1]} where parameter_id={param_id}"
            cur.execute(sql)
            con.commit()

    def UpdatePatientDiagnosis(self, patient_id:int, diag:str):
        '''Обновить диагноз пацеанта и вернуть его ИД'''
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"update patients set diagnosis = {diag} where patient_id={patient_id} returning patient_id"
            cur.execute(sql)
            patient_id = cur.fetchone()[0]
            con.commit()
        return patient_id

    def GetAllCalcRules(self):
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from calculator_rules"
            cur.execute(sql)
            rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(CalculatorRule(row[0],row[1],row[2], row[3],row[4],row[5],row[6],row[7]))
        return result

    def SaveCalcRule(self, rule:CalculatorRule):
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql = ' '.join([
                           f"insert into calculator_rules(expr, cause,recommendation,variable,value,for_sping,for_autumn)",
                           f"values('{rule.expression}','{rule.cause}','{rule.recommendation}','{rule.variable}', '{rule.value}', '{rule.for_spring}', '{rule.for_autumn}')"])
        cur.execute(sql)
        con.commit()
        cur.close()

    def UpdateCalcRule(self,rule:CalculatorRule):
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = ' '.join([
                f"update calculator_rules set expr='{rule.expression}', ",
                 f"cause='{rule.cause}',",
                 f"recommendation='{rule.recommendation}',",
                 f"variable='{rule.variable}'," ,
                 f"value='{rule.value}'," ,
                 f"for_sping={rule.for_spring},",
                 f"for_autumn={rule.for_autumn}",
                 f"where rule_id={rule.db_id} ",
                 f"returning rule_id"])
            cur.execute(sql)
            rule_id = cur.fetchone()[0]
            con.commit()
        return rule_id

    def DeleteRule(self, rule:CalculatorRule):
        con = self._create_connection_to_DB()
        cur = con.cursor()
        sql = f"delete from calculator_rules where rule_id ={rule.db_id}"
        cur.execute(sql)
        con.commit()
        cur.close()


def patient_to_dct(id:int):
    '''Функция готовит запись о пациенте к формату для передачи'''
    res = {}
    res['DATA'] = list(MainDBController.GetPatientByID(id)[0][1:-1])    #пациент без ИД и возраста
    res['DATA'][3] = str(res['DATA'][3])                                #date перевести в строку
    analysis = MainDBController.GetAllAnalysisByPatientID(id)
    res['ANALYSIS'] = {}
    for anal in analysis:
        anal_params = MainDBController.GetAllParametersByAnalysisID(anal[0])
        res['ANALYSIS'][str(anal[2])] = [[param[1], param[2], param[4]] for param in anal_params]

    return res

def dump_patient_to_json(patients_ids: list, filename='db.json'):
    data = []
    for id in patients_ids:
        data.append(patient_to_dct(id))

    json_data =  json.dumps(data, indent=4)
    with open (filename, 'w', encoding='utf-8') as file:
        file.write(json_data)


def load_data_from_json(filename='db.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data =  json.loads(file.read())
    con = MainDBController._create_connection_to_DB()
    for patient in data:
        patient_info = patient['DATA']
        with con.cursor() as cur:
            sql=' '.join([f"insert into patients(surname, name,patronymic,birthday,main_diagnosis,concomitant_diagnosis,genes, gender)",
                f"values('{patient_info[1]}','{patient_info[0]}','{patient_info[2]}','{patient_info[3]}', '{patient_info[4]}', '{patient_info[5]}', '{patient_info[6]}', '{patient_info[7]}')",
                f"returning patient_id"])
            cur.execute(sql)
            patient_id = cur.fetchone()[0]
            con.commit()

        for anal_date in patient['ANALYSIS']:
            with con.cursor() as cur:
                sql = ' '.join([f"insert into Analysis(owner_id,analysis_date)",
                            f"values({patient_id},'{anal_date}')",
                            f"returning analysis_id"])
                cur.execute(sql)
                analysis_id = cur.fetchone()[0]
                con.commit()
            MainDBController.InsertListOfParametersByAnalysisId(analysis_id, patient['ANALYSIS'][anal_date])


def dump_all_patients_to_json(filename='patients.json'):
    patients = MainDBController.GetAllPatients()
    patients_ids = [patient[0] for patient in patients]
    dump_patient_to_json(patients_ids, filename=filename)

def execute_sql(filename):
    with open(filename, encoding='utf-8') as f:
        sql = f.read()

    con = MainDBController._create_connection_to_DB()
    with con.cursor() as cur:
        cur.execute(sql)
        con.commit()


MainDBController = DBController()
