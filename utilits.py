import datetime

def date_to_sql_format(date_str):
    """Строка формата DD.MM.YYYY в sql формат YYYY-MM-DD"""
    res = date_str.split('.')
    try:
        return f'{res[2]}-{res[1]}-{res[0]}'
    except IndexError:
        print('некорректный формат ввода!')



#print(date_to_sql_format('a'))
