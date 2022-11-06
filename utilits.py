import datetime

def date_to_sql_format(date_str):
    """Строка формата DD.MM.YYYY в sql формат YYYY-MM-DD"""
    res = date_str.split('.')
    try:
        return f'{res[2]}-{res[1]}-{res[0]}'
    except IndexError:
        print('некорректный формат ввода!')

def date_sql_to_text_format(sql_date):
    """Строка формата YYYY-MM-DD в формат DD.MM.YYYY"""
    try:
        splitted_text = sql_date.split('-')
        return f'{splitted_text[2]}.{splitted_text[1]}.{splitted_text[0]}'
    except IndexError:
        return None

#print(date_to_sql_format('a'))


