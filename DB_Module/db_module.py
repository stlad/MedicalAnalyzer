import psycopg2

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
            sql = f"select * from analysis where owner_id = {patient_id}"
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
            sql = f"select * from analysis where owner_id = {patient_id} and analysis_date ='{analysis_date}'"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows


    def GetAllParameterCatalog(self):
        """Все параметры из каталога"""
        con = self._create_connection_to_DB()
        with con.cursor() as cur:
            sql = f"select * from parameter_catalog"
            cur.execute(sql)
            rows = cur.fetchall()
        return rows


def date_text_to_sql_format(text):
    try:
        splitted_text = text.split('.')
        return f'{splitted_text[2]}-{splitted_text[1]}-{splitted_text[0]}'
    except IndexError:
        return None

MainDBController = DBController()


#print(date_text_to_sql_format('asdasd'))
'''rows = MainDBController.GetAllPatients()

for r in rows:
    print(r)'''
#MainBDUser.InsertPatinet(['Пучков','Дмитрий','Юрьевич','1961-11-25','что-то страшное','что-тоужасное',''])
#print(MainBDUser.GetAllPatients())
#print(MainDBController.GetAllAnalysisByPatinetIDandDate(2,'2001-11-10'))

