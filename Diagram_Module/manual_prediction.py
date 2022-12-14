# - (min/false)
# = (norm)
# + (max/true)
# * (none)
# 1/2/3/4 (stage: 1-4)

# [0] neu/lymf,
# [1] neu/cd3,
# [2] neu/cd4,
# [3] neu/cd8,
# [4] lymf/cd19,
# [5] cd19/cd4,
# [6] cd19/cd8,
# [7] ovid_stage,
# [8] b_plus_tnk_to_02,
# [9] cd4_more_05,
# [10] cd4_cd8_more_1,
# [11] cd4_more_02_less_05,
# [12] cd4_more_009_less_019,
# [13] cd4_more_005_less_0089
# : 'diagnose'

# conditions_sets = {
#     ['', '', '', '', '', '', '', '', '', '', '', '', '']: 'ОВИД, можно компенсировать',
#     ['', '', '', '', '', '', '', '', '', '', '', '', '']: 'ОВИД, можно компенсировать',
#     ['', '', '', '', '', '', '', '', '', '', '', '', '']: 'ОВИД, требуется наблюдение инфекционной реакции',
#     ['', '', '', '', '', '', '', '', '', '', '', '',
#      '']: 'Пациент скомпенсирован по Т-звену и сдает иммунограмму через 6 мес',
#     ['', '', '', '', '', '', '', '', '', '', '', '',
#      '']: 'ТКИД 2 степени - стимулировать т клеточное звено и наблюдать за отклонением',
#     ['', '', '', '', '', '', '', '', '', '', '', '', '']: 'ТКИД 3 степени - стимулировать т клеточное звено',
#     ['', '', '', '', '', '', '', '', '', '', '', '', '']: 'ТКИД 4 степени - гематологический диагноз',
#     # ['', '', '', '', '', '', '', '', '', '', '', '', '', '']: '',
# }
# CD8 = {'min': 0.5, 'max': 0.9}
# CD4 = {'min': 0.7, 'max': 1.1}
import operator
import pandas as pd

def split_to_conditions_and_unions(string):
    brackets_counter = 0
    sub_strings = []
    unions = []
    ss_start_idx = -1
    for i in range(len(string)):
        if string[i] == '(':
            if brackets_counter == 0:
                ss_start_idx = i + 1
                brackets_counter = 1
                while brackets_counter > 0 and i < len(string):
                    i += 1
                    if string[i] == '(':
                        brackets_counter += 1
                    elif string[i] == ')':
                        brackets_counter -= 1
                        if brackets_counter == 0:
                            sub_strings.append(string[ss_start_idx:(i - 1)])
                            ss_start_idx = -1
        elif brackets_counter == 0 and string[i] == ')':
            raise Exception(
                "Ошибка: Закрывающая скобочка без открывающей.")
        elif string[i] != ' ':
            if string.startswith('and', i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:(i - 1)])
                    ss_start_idx = -1
                unions.append('and')
                i += 2
            elif string.startswith('or', i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:(i - 1)])
                    ss_start_idx = -1
                unions.append('or')
                i += 1
            elif ss_start_idx == -1:
                ss_start_idx = i
            elif i == len(string) - 1:
                sub_strings.append(string[ss_start_idx:i])
    return sub_strings, unions


# Нет обработки ошибочного ввода
def get_val(element, data):
    patient = data[list(data.keys())[0]]
    analysis = patient[list(patient.keys())[0]]
    analysis_keys = list(analysis.keys())
    try:
        return float(element)
    except ValueError:
        for a in analysis_keys:
            if a.__contains__(element):
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
    for i in range(len(condition)):
        for o in list(operators.keys()):
            if condition.startswith(o):
                left = get_val(condition[0:(i - 1)].replace(' ', ''), data)
                right = get_val(condition[(i + len(o)):].replace(' ', ''), data)
                return operators[o](left, right)
    raise Exception("Ошибка: неправильный оператор сравнения.")


def get_condition_result(condition, data):
    conditions = [condition]
    unions = []
    if condition.__contains__('and') or condition.__contains__('or'):
        conditions, unions = split_to_conditions_and_unions(condition)
        result = get_condition_result(conditions[0])
        for i in range(1, len(conditions)):
            if unions[i - 1] == 'and':
                result = result and get_condition_result(conditions[i])
            else:
                result = result or get_condition_result(conditions[i])
        return result
    else:
        return evaluate_condition(condition, data)


def predict_by_xlsx(path, dct):
    data = pd.read_excel(path)
    for i in range(len(data['Диагноз'])):
        if get_condition_result(data['Выражение'][i], dct):
            return data['Диагноз'][i]
    return 'Требуется дополнительный анализ данных с использованием нейронной сети.'
