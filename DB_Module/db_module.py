import psycopg2


def create_connection_to_DB(database, user, password, host, port):
    '''Создает соединение с базоый данных и возвращает его'''
    try:
        con = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Database opened successfully!")
        return con
    except psycopg2.OperationalError:
        print('Не получилось подключиться к базе данных')
        return



class DB_controller:
    def __init__(self):
        self.con = create_connection_to_DB('MedicalAnalysis_DB', 'postgres', 'admin', 'localhost', '5432')


CON = DB_controller()