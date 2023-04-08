import math


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
        result += "\t{} - {}\n".format(key, w2)
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
    text_result = add_to_string(text_result, result, "Показатели B - клеточного звена иммунитета:")
    result.clear()
    result["NEU/CD3"] = [2.25, NEU / CD3, 3.63]
    result["NEU/LYMF"] = [1.67, NEU / LYMF, 1.8]
    result["NEU/CD4"] = [3, NEU / CD4, 5]
    result["NEU/CD8"] = [9.47, NEU / CD8, 12.3]
    text_result = add_to_string(text_result, result, "Показатели T - клеточного звена иммунитета:")
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
    text_result = add_to_string(text_result, result, "Цитокиновые пары:")
    return text_result
