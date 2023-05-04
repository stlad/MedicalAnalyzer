import math
import operator
import pandas as pd


def add_to_string(str, dic, name):
    result = str
    result += "{}\n".format(name)
    keys = list(dic.keys())
    for key in keys:
        words = ["в пределах 20% отклонения {}", "отклонение более 20% {}", "в пределах нормы"]
        val = dic[key]
        if val[1] >= val[2]:
            nav = "вверх"
            d1 = val[1] - val[2]
            d2 = (val[2] - val[0]) / 5 + val[2]
            if d1 < d2:
                w2 = words[0].format(nav)
            else:
                w2 = words[1].format(nav)
        elif val[0] >= val[1]:
            nav = "вниз"
            d1 = val[1] - val[2]
            d2 = val[0] - ((val[2] - val[0]) / 5)
            if d1 > d2:
                w2 = words[0].format(nav)
            else:
                w2 = words[1].format(nav)
        else:
            w2 = words[2]
        result += "{} - {}\n".format(key, w2)
    return result


def check_statuses(data):
    name = list(data.keys())[0]
    data = data[name]
    date = list(data.keys())[0]
    data = data[date]
    result = {}
    NEU = data['Нейтрофилы (NEU)']['Результат']
    LYMF = data['Лимфоциты (LYMF)']['Результат']
    CD3 = data['Общие T-лимфоциты (CD45+CD3+)']['Результат']
    CD4 = data['Т-хелперы (CD45+CD3+CD4+)']['Результат']
    CD8 = data['Т-цитотоксические лимфоциты (CD45+CD3+СD8+)']['Результат']
    CD19 = data['Общие В-лимфоциты (CD45+CD19+)']['Результат']
    text_result = ""
    result["NEU/LYMF"] = [1.67, NEU / LYMF, 1.8]
    result["LYMF/CD19"] = [9.6, LYMF / CD19, 10]
    result["CD19/CD4"] = [0.16, CD19 / CD4, 0.31]
    result["CD19/CD8"] = [0.53, CD19 / CD8, 0.77]
    add_to_string(text_result, result, "Показатели B - клеточного звена иммунитета")
    result.clear()
    result["NEU/CD3"] = [2.25, NEU / CD3, 3.63]
    result["NEU/LYMF"] = [1.67, NEU / LYMF, 1.8]
    result["NEU/CD4"] = [3, NEU / CD4, 5]
    result["NEU/CD8"] = [9.47, NEU / CD8, 12.3]
    add_to_string(text_result, result, "Показатели T - клеточного звена иммунитета")
    result.clear()
    if data['CD3+TNFa+(спонтанный)']['Результат'] == 0:
        fno_res = 0
    else:
        fno_res = data['CD3+TNFa+(стимулированный)']['Результат'] / data['CD3+TNFa+(спонтанный)']['Результат']
    result["ФНО"] = [80, fno_res, 120]
    if data['CD3+IFNy+(спонтанный)']['Результат'] == 0:
        infer_res = 0
    else:
        infer_res = data['CD3+IFNy+(стимулированный)']['Результат'] / data['CD3+IFNy+(спонтанный)']['Результат']
    result["Интерферон"] = [0, infer_res, 18.6 / 0.5]
    if data['CD3+IL2+(спонтанный)']['Результат'] == 0:
        inlik_res = 0
    else:
        inlik_res = data['CD3+IL2+(стимулированный)']['Результат'] / data['CD3+IL2+(спонтанный)']['Результат']
    result["Интерликин"] = [0, inlik_res, 45.7 / 0.5]
    add_to_string(text_result, result, "Цитокиновые пары")
    return text_result


# # Недостаток CD4 –нужно корректировать через стимуляторы Т-клеточного звена (Т-активин и аналоги)
# def check_CD4(data):
#     name = list(data.keys())[0]
#     data = data[name]
#     date = list(data.keys())[0]
#     data = data[date]
#     CD4 = data['Т-хелперы (CD45+CD3+CD4+)']['Результат']
#     if CD4 < 0.7:
#         return True
#     return False
#
#
# # Анализируем НСТ сп и НСТ ст. ТОЛЬКО для весны! Отношение этих значений должно быть 1 к 10 и нет сахарного диабета, то назначать глюкозу и витамин С.
# def check_NST(data):
#     name = list(data.keys())[0]
#     data = data[name]
#     date = list(data.keys())[0]
#     if not date.split('-')[1] in ['03', '04', '05']:
#         return False
#     data = data[date]
#     NST_sp = data['НСТ-тест (спонтанный)']['Результат']
#     NST_st = data['НСТ-тест (стимулированный)']['Результат']
#     if NST_st >= (NST_sp * 10):
#         return True
#     return False
#
#
# # Смотрим ЦИК. Если <50, то назначаем глюкозу+витамин С
# def check_CIK(data):
#     name = list(data.keys())[0]
#     data = data[name]
#     date = list(data.keys())[0]
#     data = data[date]
#     CIK = data['Циркулирующие иммунные комплексы']['Результат']
#     if CIK < 50:
#         return True
#     return False


def check_base_diagnoses(path, data):
    i = 1
    result = ""
    def_text = "Рекомендация {}:\n\tТип: {}\n\tПричина: {}\n\tРекомендация: {}\n"
    # if check_CD4(data):
    #     result += def_text.format(i, 'по одному диагнозу', 'Т-хелперы менее 0.7', 'Т-активин и аналоги)')
    #     i += 1
    # if check_NST(data):
    #     result += def_text.format(i, 'по одному диагнозу',
    #                               'НСТ-спонтанный в десять или более раз меньше НСТ-стимулированного',
    #                               'при отсутствии диабета, назначать глюкозу и витамин С')
    #     i += 1
    # if check_CIK(data):
    #     result += def_text.format(i, 'по одному диагнозу', 'циркулирующие иммунные комплексы меньше пятидесяти',
    #                               'назначаются глюкоза и витамин С')
    #     i += 1
    try:
        resultsx = predict_by_xlsx(path, data)
        if resultsx.__len__() > 0:
            for res in resultsx:
                result += def_text.format(i, 'по одному диагнозу', res[0], res[1])
                i += 1
    except Exception as e:
        print(e)
    return result


# Псевдокод..................................................................................................

def split_to_conditions_and_unions(string):
    brackets_counter = 0
    sub_strings = []
    unions = []
    ss_start_idx = -1
    i = 0
    while i < len(string):
        if string[i] == '(':
            ss_start_idx = i + 1
            brackets_counter = 1
            while brackets_counter > 0 and i + 1 < len(string):
                i += 1
                if string[i] == '(':
                    brackets_counter += 1
                elif string[i] == ')':
                    brackets_counter -= 1
                if brackets_counter == 0:
                    sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
                    ss_start_idx = -1
                elif i + 1 >= len(string):
                    raise Exception(
                        "Ошибка: Отсутствует закрывающая скобочка.")
        elif string[i] == ')':
            raise Exception(
                "Ошибка: Закрывающая скобочка без открывающей.")
        elif string[i] != ' ':
            if string.startswith('and', i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
                    ss_start_idx = -1
                unions.append('and')
                i += 2
            elif string.startswith('or', i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
                    ss_start_idx = -1
                unions.append('or')
                i += 1
            elif ss_start_idx == -1:
                ss_start_idx = i
            elif i == len(string) - 1:
                sub_strings.append(string[ss_start_idx + len(unions[-1]) - 1:i + 1].replace(' ', ''))
        i += 1
    return sub_strings, unions


def get_val(element, data):
    if element.__contains__('/'):
        sub_el = element.split('/')
        return get_val(sub_el[0], data) / get_val(sub_el[1], data)
    elif element.__contains__('*'):
        sub_el = element.split('/')
        return get_val(sub_el[0], data) * get_val(sub_el[1], data)
    patient = data[list(data.keys())[0]]
    analysis = patient[list(patient.keys())[0]]
    analysis_keys = list(analysis.keys())
    try:
        return float(element)
    except ValueError:
        for a in analysis_keys:
            a_c = a.replace('С', 'C')
            if element in a_c:
                return float(analysis[a]['Результат'])


def evaluate_condition(condition, data):
    operators = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge
    }
    op = None
    idx = -1
    for o in list(operators.keys()):
        idx = condition.find(o)
        if idx != -1:
            op = o
            break
    if op is not None:
        left = get_val(condition[0:idx].replace(' ', ''), data)
        right = get_val(condition[(idx + len(op)):].replace(' ', ''), data)
        return operators[op](left, right)
    raise Exception("Ошибка: неправильный оператор сравнения.")


def get_condition_result(condition, data):
    conditions = [condition]
    unions = []
    if condition.__contains__('and') or condition.__contains__('or'):
        conditions, unions = split_to_conditions_and_unions(condition)
        result = get_condition_result(conditions[0], data)
        for i in range(1, len(conditions)):
            if unions[i - 1] == 'and':
                result = result and get_condition_result(conditions[i], data)
            else:
                result = result or get_condition_result(conditions[i], data)
        return result
    else:
        return evaluate_condition(condition, data)


def check_for_spring(spring, dct):
    if not spring:
        return True
    name = list(dct.keys())[0]
    data = dct[name]
    date = list(data.keys())[0]
    if not date.split('-')[1] in ['03', '04', '05']:
        return False
    return True


def check_for_autumn(autumn, dct):
    if not autumn:
        return True
    name = list(dct.keys())[0]
    data = dct[name]
    date = list(data.keys())[0]
    if not date.split('-')[1] in ['09', '10', '11']:
        return False
    return True


def predict_by_xlsx(path, dct):
    data = pd.read_excel(path)
    variables = {}
    result = []
    for i in range(len(data['Переменная'])):
        variables[data['Переменная'][i]] = data['Значение'][i]
    for i in range(len(data['Рекомендации'])):
        cond = data['Выражение'][i]
        j = 0
        l = len(cond)
        while j < l:
            for v_k in list(variables.keys()):
                if j + len(v_k) < l and cond.startswith(v_k, j) and (j + len(v_k) >= len(cond) or (
                        cond[j + len(v_k)] != '+' and not cond[j + len(v_k)].isnumeric())):
                    l = l - len(v_k) + len(variables[v_k])
                    cond = cond[0:j] + variables[v_k] + cond[j + len(v_k):]
            j += 1
        if get_condition_result(cond, dct) and check_for_spring(data['Только весна'] == 'Да', dct) and check_for_autumn(
                data['Только осень'] == 'Да', dct):
            result.append((data['Причина'][i], data['Рекомендации'][i]))
    return result
