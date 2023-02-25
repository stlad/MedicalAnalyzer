import operator
import pandas as pd


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


def predict_by_xlsx(path, dct):
    data = pd.read_excel(path)
    variables = {}
    for i in range(len(data['Переменная'])):
        variables[data['Переменная'][i]] = data['Значение'][i]
    for i in range(len(data['Диагноз'])):
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
        if get_condition_result(cond, dct):
            return data['Диагноз'][i]
    return 'Требуется дополнительный анализ данных с использованием нейронной сети.'
