import psycopg2

class DB_user():
    def __init__(self,database = 'MedicalAnalysis_DB', user = 'postgres', password='admin', host='localhost', port='5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        print('User Entered successfully!')

    def create_connection_to_DB(self):
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


def date_text_to_sql_format(text):
    splitted_text = text.split('.')
    return f'{splitted_text[2]}-{splitted_text[1]}-{splitted_text[0]}'


MainBDUser = DB_user()