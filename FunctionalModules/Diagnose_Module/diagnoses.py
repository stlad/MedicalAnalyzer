import pandas as pd

ops = {
    "and": "[и]",
    "or": "[или]",
    "==": "[==]",
    "<=": "[<=]",
    ">=": "[>=]",
    "!=": "[!=]",
    "<": "[<]",
    ">": "[>]",
    "+": "[+]",
    "-": "[-]",
    "*": "[*]",
    "/": "[/]",
    "^": "[^]",
}


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


def check_diagnoses(conditions, data):
    conditions_d = {"Выражение": [], "Только весна": [], "Только осень": [], "Причина": [], "Рекомендации": []}
    var_val = {}
    for c in conditions:
        var_val[c.variable] = c.value
        if c.recommendation != "":
            conditions_d["Выражение"].append(c.expression)
            conditions_d["Причина"].append(c.cause)
            conditions_d["Рекомендации"].append(c.recommendation)
            conditions_d["Только весна"].append(c.for_spring)
            conditions_d["Только осень"].append(c.for_autumn)
    i = 1
    result = ""
    def_text = "Рекомендация {}:\n\tТип: {}\n\tПричина: {}\n\tРекомендация: {}\n"
    try:
        resultsx = get_diagnose(conditions_d, var_val, data)
        if resultsx.__len__() > 0:
            for res in resultsx:
                result += def_text.format(i, 'по одному диагнозу', res[0], res[1])
                i += 1
    except Exception as e:
        print(e)
    return result


# Псевдокод..................................................................................................

def split_to_conditions_and_unions(string):
    # brackets_counter = 0
    sub_strings = []
    unions = []
    ss_start_idx = -1
    i = 0
    while i < len(string):
        # if string[i] == '(':
        #     ss_start_idx = i + 1
        #     brackets_counter = 1
        #     while brackets_counter > 0 and i + 1 < len(string):
        #         i += 1
        #         if string[i] == '(':
        #             brackets_counter += 1
        #         elif string[i] == ')':
        #             brackets_counter -= 1
        #         if brackets_counter == 0:
        #             sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
        #             ss_start_idx = -1
        #         elif i + 1 >= len(string):
        #             raise Exception(
        #                 "Ошибка: Отсутствует закрывающая скобочка.")
        # elif string[i] == ')':
        #     raise Exception(
        #         "Ошибка: Закрывающая скобочка без открывающей.")
        # elif string[i] != ' ':
        if string[i] != ' ':
            if string.startswith(ops['and'], i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
                    ss_start_idx = -1
                unions.append(ops['and'])
                i += len(ops['and']) - 1
            elif string.startswith(ops['or'], i):
                if ss_start_idx != -1:
                    sub_strings.append(string[ss_start_idx:i].replace(' ', ''))
                    ss_start_idx = -1
                unions.append(ops['or'])
                i += len(ops['or']) - 1
            elif ss_start_idx == -1:
                ss_start_idx = i
            elif i == len(string) - 1:
                sub_strings.append(string[ss_start_idx:].replace(' ', ''))
        i += 1
    return sub_strings, unions


def prepare_string_to_compare(str):
    return str.replace(' ', '').lower().replace('c', 'с').replace('h', 'н').replace('x', 'х').replace('o', 'о')


def get_val(element, data):
    if element.__contains__(ops['/']):
        sub_el = element.split(ops['/'])
        return get_val(sub_el[0], data) / get_val(sub_el[1], data)
    elif element.__contains__(ops['*']):
        sub_el = element.split(ops['*'])
        return get_val(sub_el[0], data) * get_val(sub_el[1], data)
    elif element.__contains__(ops['+']):
        sub_el = element.split(ops['+'])
        return get_val(sub_el[0], data) + get_val(sub_el[1], data)
    elif element.__contains__(ops['-']):
        sub_el = element.split(ops['-'])
        return get_val(sub_el[0], data) - get_val(sub_el[1], data)
    elif element.__contains__(ops['^']):
        sub_el = element.split(ops['^'])
        return get_val(sub_el[0], data) ** get_val(sub_el[1], data)
    patient = data[list(data.keys())[0]]
    analysis = patient[list(patient.keys())[0]]
    analysis_keys = list(analysis.keys())
    try:
        return float(element)
    except ValueError:
        for a in analysis_keys:
            a_с = prepare_string_to_compare(a)
            element = prepare_string_to_compare(element)
            if element in a_с:
                return float(analysis[a]['Результат'])


def evaluate_condition(condition, data):
    operators = {
        ops['<=']: lambda a, b: float(a) <= float(b),
        ops['==']: lambda a, b: float(a) == float(b),
        ops['!=']: lambda a, b: float(a) != float(b),
        ops['>=']: lambda a, b: float(a) >= float(b),
        ops['<']: lambda a, b: float(a) < float(b),
        ops['>']: lambda a, b: float(a) > float(b),
    }
    op = None
    idx = -1
    for o in list(operators.keys()):
        idx = condition.find(o)
        if idx != -1:
            op = o
            break
    if op is not None:
        # cond.replace(' ', '')
        left = get_val(condition[0:idx], data)
        right = get_val(condition[(idx + len(op)):], data)
        result = operators[op](left, right)
        return result
    raise Exception("Ошибка: неправильный оператор сравнения.")


def get_condition_result(condition, data):
    conditions = [condition]
    unions = []
    if condition.__contains__(ops['and']) or condition.__contains__(ops['or']):
        conditions, unions = split_to_conditions_and_unions(condition)
        result = get_condition_result(conditions[0], data)
        if len(conditions) > 1:
            for i in range(1, len(conditions)):
                if unions[i - 1] == ops['and']:
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


def get_diagnose(conditions, variables, dct):
    result = []
    for i in range(len(conditions["Выражение"])):
        cond = conditions['Выражение'][i]
        j = 0
        # l = len(cond)
        while j < len(cond):
            for v_k in list(variables.keys()):
                # if j + len(v_k) < l and cond.startswith(v_k, j) and (j + len(v_k) >= len(cond) or (
                #         cond[j + len(v_k)] != ops['+'] and not cond[j + len(v_k)].isnumeric())):
                #     l = l - len(v_k) + len(variables[v_k])
                #     cond = cond[0:j] + variables[v_k] + cond[j + len(v_k):]
                if v_k != "" and cond.startswith(v_k, j):
                    cond = cond[0:j] + variables[v_k] + cond[j + len(v_k):]
                    j += len(variables[v_k]) - 1
                    break
            j += 1

        if get_condition_result(cond, dct) and (
                not conditions['Только весна'][i] or check_for_spring(conditions['Только весна'][i], dct)
                and (not conditions['Только осень'][i] or check_for_autumn(conditions['Только осень'][i], dct))):
            result.append((conditions['Причина'][i], conditions['Рекомендации'][i]))
    return result
