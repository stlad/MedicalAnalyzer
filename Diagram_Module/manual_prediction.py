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

NEU_LYMF = {'min': 1.67, 'max': 1.8}
NEU_CD3 = {'min': 2.25, 'max': 3.63}
NEU_CD4 = {'min': 3.0, 'max': 5.0}
NEU_CD8 = {'min': 9.47, 'max': 12.3}
# LYMF_CD19 = {'min': 9.6, 'max': 10.0}
# CD19_CD4 = {'min': 0.16, 'max': 0.31}
# CD19_CD8 = {'min': 0.53, 'max': 0.77}


def get_ovid(analysis):
    b_lymf = analysis['Общие В-лимфоциты (CD45+CD19+)']['Результат']
    if b_lymf <= 0.039:
        return 4
    elif b_lymf <= 0.06:
        return 3
    elif b_lymf <= 0.11:
        return 2
    elif b_lymf <= 0.2:
        return 1
    elif b_lymf <= 0.5:
        return 0
    else:
        return -1


def check_tnk_b_sum(analysis):
    b_lymf = analysis['Общие В-лимфоциты (CD45+CD19+)']['Результат']
    tnk = analysis['Общие NK-клетки (CD45+CD3-CD16+56+)']['Результат']
    s = tnk + b_lymf
    if s < 0.2:
        return False
    else:
        return True


def T_cells_is_sick(analysis):
    NEU = analysis['Нейтрофилы (NEU)']['Результат']
    LYMF = analysis['Лимфоциты (LYMF)']['Результат']
    CD3 = analysis['Общие T-лимфоциты (CD45+CD3+)']['Результат']
    CD4 = analysis['Т-хелперы (CD45+CD3+CD4+)']['Результат']
    CD8 = analysis['Т-цитотоксические лимфоциты (CD45+CD3+СD8+)']['Результат']
    return NEU_LYMF['min'] <= NEU / LYMF <= NEU_LYMF['max'] and NEU_CD3['min'] <= NEU / CD3 <= NEU_CD3['max'] and \
           NEU_CD4['min'] <= NEU / CD4 <= NEU_CD4['max'] and NEU_CD8['min'] <= NEU / CD8 <= NEU_CD8['max']


def get_diagnose(data):
    patient = data[list(data.keys())[0]]
    analysis = patient[list(patient.keys())[0]]
    ovid = get_ovid(analysis)
    if ovid > 0:
        if check_tnk_b_sum(analysis):
            return 'ОВИД {}. Можно компенсировать.'.format(ovid)
        else:
            return 'ОВИД {}. Требуется наблюдение инфекционной реакции.'.format(ovid)
    CD4 = analysis['Т-хелперы (CD45+CD3+CD4+)']['Результат']
    CD8 = analysis['Т-цитотоксические лимфоциты (CD45+CD3+СD8+)']['Результат']
    if T_cells_is_sick(analysis) and CD4/CD8 > 1:
        if 0.05 <= CD4 <= 0.09:
            return 'ТКИД 4 степени - гематологический диагноз'
        elif CD4 <= 0.2:
            return 'ТКИД 3 степени - стимулировать т клеточное звено'
        elif CD4 <= 0.5:
            return 'ТКИД 2 степени - стимулировать т клеточное звено и наблюдать за отклонением (восстановилось или нет)'
        elif CD4 > 0.5:
            return 'Хорошо (пациент скомпенсирован по Т-звену) и сдает иммунограм через 6 мес.'
    if ovid < 0:
        return 'Требуется дополнительный анализ. В 40 лет и старше множественная аллергия, ревматоидные артриты, бронхоэктатическая болень и в интервале 20 лет переходит в В-лимфому'
    return 'Требуется дополнительный анализ.'