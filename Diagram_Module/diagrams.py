import json, math, os
from copy import copy

import numpy as np
import pylab as pl
from matplotlib import pyplot as plt
import pandas as pd

def reduce_dec_num(val):
    return math.ceil(val * 10) / 10


class Radar(object):

    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            rect = [0.15, 0.1, 0.70, 0.70]

        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i)
                     for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=12)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, 6), angle=angle, labels=label)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 6.5)

    def plot(self, values, names, maxs, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)
        for i in range(len(names)):
            self.ax.annotate(names[i],
                             xy=(angle[i], values[i]),  # theta, radius
                             xytext=(angle[i] + 0.5, values[i]),  # fraction, fraction
                             arrowprops=dict(facecolor='black', arrowstyle="->", linewidth=1),
                             fontsize=9,
                             )


def get_age_ending(age):
    if age // 10 == 1:
        return 'год'
    elif 2 <= age // 10 <= 4:
        return 'года'
    return 'лет'


def make_radar_diagram(data, title):
    names = data['names']
    fig = pl.figure(figsize=(6, 6))
    vals = (data['min'], data['res'], data['max'])
    labels = ("Нижние референтные значения", 'Результаты', "Верхние референтные значения")
    colors = ("g", "r", "g")
    ranges = []
    graph_max = []
    for i in range(len(data['res'])):
        graph_max.append(math.ceil(max((data['min'][i], data['res'][i], data['max'][i]))))
        ranges.append([])
        for j in range(5):
            ranges[i].append(round((j + 1) * (graph_max[i] / 5), 2))

    titles = list(names)

    radar = Radar(fig, titles, ranges)
    for i in range(len(vals)):
        prepared_vals = []
        for j in range(len(vals[i])):
            prepared_vals.append(vals[i][j] / graph_max[j] * 5)
        radar.plot(prepared_vals, vals[i], graph_max, "-", lw=2, color=colors[i], alpha=1, label=labels[i])
    radar.ax.legend(loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
    pl.title(title, pad=40)
    return fig


def make_radars(data, name, date, age, diagnos):
    diagram_types = ['Показатели В - клеточного звена иммунитета', 'Показатели T - клеточного звена иммунитета']
    fig = make_radar_diagram(
        data['b'],
        "Пациент: {} \n"
        "Возраст на момент сдачи анализов: {} {}. \n"
        "Дата сдачи анализов: {}\n"
        "Диагноз: {}\n"
        "График: {}".format(
            name, #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
            #'. '.join([i[0] for i in name.split()]),
            age, get_age_ending(age),
            date,
            diagnos,
            diagram_types[0]
        ))

    fig1 = make_radar_diagram(
        data['t'],
        "Пациент: {} \n"
        "Возраст на момент сдачи анализов: {} {}. \n"
        "Дата сдачи анализов: {}\n"
        "Диагноз: {}\n"
        "График: {}".format(
            name, #ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ
            #'. '.join([i[0] for i in name.split()]),
            age, get_age_ending(age),
            date,
            diagnos,
            diagram_types[1]
        ))
    return fig, fig1


def make_time_diagram(arr, dates, labels, diagram_type, name, spring_idxs, automn_idxs, over_idxs, season_over_idxs):
    fig, ax = plt.subplots(figsize=(len(arr), len(dates)))
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'black', 'yellow']
    for i in range(len(arr)):
        linestyle = 'solid'
        if i % 3 >= 1:
            linestyle = 'dashed'
        ax.plot(dates, arr[i], label=labels[i], color=colors[i // 3], linestyle=linestyle)
    for i in range(len(arr)):
        for j in range(len(over_idxs[i])):
            ax.plot(dates[over_idxs[i][j]], arr[i][over_idxs[i][j]], "s", color=colors[i // 3])
        for j in range(len(season_over_idxs[i])):
            ax.plot(dates[season_over_idxs[i][j]], arr[i][season_over_idxs[i][j]], "*", markersize=11, color=colors[i // 3])
    for i in range(len(spring_idxs)):
        ax.axvspan(spring_idxs[i] - 0.5, spring_idxs[i] + 0.5, facecolor='g', alpha=0.05)
    for i in range(len(automn_idxs)):
        ax.axvspan(automn_idxs[i] - 0.5, automn_idxs[i] + 0.5, facecolor='orange', alpha=0.05)
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(rotation=40)
    plt.title("Пациент: {}\nГрафик: {}".format( name[0], diagram_type), pad=0)#ТУТ ИСПОЛЬЗУЮТСЯ ИНИЦИАЛЫ ДЛЯ ЗАЩИТЫ было '. '.join([i[0] for i in name.split()])
    plt.subplots_adjust(left=-0.001, right=0.85, top=0.9, bottom=0.17)
    return fig


def prepare_data(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
    return dic_prepare_data(data)


def make_time_diagrams(data, dates, name):
    keys = list(data['t'].keys())
    arr = []
    over = []
    season_over = []
    spring_idxs = []
    automn_idxs = []

    for i in range(len(keys)):
        if i % 3 == 0:
            vals = data['t'][keys[i]]
            vals_mins = data['t'][keys[i + 1]]
            vals_maxs = data['t'][keys[i + 2]]
            arr.append(data['t'][keys[i]])
            arr.append(data['t'][keys[i + 1]])
            arr.append(data['t'][keys[i + 2]])
            over.append([])
            over.append([])
            over.append([])
            season_over.append([])
            season_over.append([])
            season_over.append([])
            for j in range(len(data['t'][keys[i]])):
                delta = vals_maxs[0] - vals_mins[0]
                if ['01','02','03','04','05','06'].__contains__(dates[j].split('-')[1]):
                    #spring
                    spring_idxs.append(j)
                    if vals[j] > vals_maxs[0] + delta * 0.25:
                        season_over[i].append(j)
                    elif vals[j] > vals_maxs[0]:
                        over[i].append(j)
                    elif vals[j] < vals_mins[0]:
                        season_over[i].append(j)
                else:
                    #automn
                    automn_idxs.append(j)
                    if vals[j] < vals_mins[0] - delta * 0.25:
                        season_over[i].append(j)
                    elif vals[j] > vals_maxs[0]:
                        season_over[i].append(j)
                    elif vals[j] < vals_mins[0]:
                        over[i].append(j)
    # for key in keys:
    #     arr.append(data['t'][key])

    fig = make_time_diagram(arr, dates, keys, 'Т-клеточное звено', name, spring_idxs, automn_idxs, over, season_over)
    # save_and_close(fig, path,  'Т-клеточное звено')

    keys = list(data['b'].keys())
    arr = []
    over = []
    season_over = []
    spring_idxs = []
    automn_idxs = []

    for i in range(len(keys)):
        if i % 3 == 0:
            vals = data['b'][keys[i]]
            vals_mins = data['b'][keys[i + 1]]
            vals_maxs = data['b'][keys[i + 2]]
            arr.append(data['b'][keys[i]])
            arr.append(data['b'][keys[i + 1]])
            arr.append(data['b'][keys[i + 2]])
            over.append([])
            over.append([])
            over.append([])
            season_over.append([])
            season_over.append([])
            season_over.append([])
            for j in range(len(data['b'][keys[i]])):
                delta = vals_maxs[0] - vals_mins[0]
                if ['01', '02', '03', '04', '05', '06'].__contains__(dates[j].split('-')[1]):
                    # spring
                    spring_idxs.append(j)
                    if vals[j] > vals_maxs[0] + delta * 0.25:
                        season_over[i].append(j)
                    elif vals[j] > vals_maxs[0]:
                        over[i].append(j)
                    elif vals[j] < vals_mins[0]:
                        season_over[i].append(j)
                else:
                    # automn
                    automn_idxs.append(j)
                    if vals[j] < vals_mins[0] - delta * 0.25:
                        season_over[i].append(j)
                    elif vals[j] > vals_maxs[0]:
                        season_over[i].append(j)
                    elif vals[j] < vals_mins[0]:
                        over[i].append(j)
    fig1 = make_time_diagram(arr, dates, keys, 'B-клеточное звено', name, spring_idxs, automn_idxs, over, season_over)
    # save_and_close(fig1, path, 'B-клеточное звено')
    return fig, fig1


def dic_prepare_data(data):
    name = list(data.keys())[0]
    data = data[name]

    dates = list(data.keys())
    ages = []
    diagnoses = []
    for d in dates:
        ages.append(data[d]['Возраст'])
        diagnoses.append(data[d]['Диагноз'])
    line_data = {
        't': {
            'CD8': [],
            'ref_min_CD8': [],
            'ref_max_CD8': [],
            'CD4': [],
            'ref_min_CD4': [],
            'ref_max_CD4': [],
            'NEU / LYMF': [],
            'ref_min_NEU/LYMF': [],
            'ref_max_NEU/LYMF': [],
            'NEU / CD3': [],
            'ref_min_NEU/CD3': [],
            'ref_max_NEU/CD3': [],
            'NEU / CD4': [],
            'ref_min_NEU/CD4': [],
            'ref_max_NEU/CD4': [],
            'NEU / CD8': [],
            'ref_min_NEU/CD8': [],
            'ref_max_NEU/CD8': [],
        },
        'b': {
            'CD8': [],
            'ref_min_CD8': [],
            'ref_max_CD8': [],
            'CD4': [],
            'ref_min_CD4': [],
            'ref_max_CD4': [],
            'NEU / LYMF': [],
            'ref_min_NEU/LYMF': [],
            'ref_max_NEU/LYMF': [],
            'LYMF / CD19': [],
            'ref_min_LYMF/CD19': [],
            'ref_max_LYMF/CD19': [],
            'CD19 / CD4': [],
            'ref_min_CD19/CD4': [],
            'ref_max_CD19/CD4': [],
            'CD19 / CD8': [],
            'ref_min_CD19/CD8': [],
            'ref_max_CD19/CD8': [],
        }
    }
    radars_data = []
    for date in dates:
        line_data['t']['ref_min_CD8'].append(0.5)
        line_data['t']['ref_max_CD8'].append(0.9)
        line_data['t']['ref_min_CD4'].append(0.7)
        line_data['t']['ref_max_CD4'].append(1.1)
        line_data['t']['ref_min_NEU/LYMF'].append(1.67)
        line_data['t']['ref_max_NEU/LYMF'].append(1.8)
        line_data['t']['ref_min_NEU/CD3'].append(2.25)
        line_data['t']['ref_max_NEU/CD3'].append(3.63)
        line_data['t']['ref_min_NEU/CD4'].append(3)
        line_data['t']['ref_max_NEU/CD4'].append(5)
        line_data['t']['ref_min_NEU/CD8'].append(9.47)
        line_data['t']['ref_max_NEU/CD8'].append(12.3)

        line_data['b']['ref_min_CD8'].append(0.5)
        line_data['b']['ref_max_CD8'].append(0.9)
        line_data['b']['ref_min_CD4'].append(0.7)
        line_data['b']['ref_max_CD4'].append(1.1)
        line_data['b']['ref_min_NEU/LYMF'].append(1.67)
        line_data['b']['ref_max_NEU/LYMF'].append(1.8)
        line_data['b']['ref_min_LYMF/CD19'].append(9.6)
        line_data['b']['ref_max_LYMF/CD19'].append(10)
        line_data['b']['ref_min_CD19/CD4'].append(0.16)
        line_data['b']['ref_max_CD19/CD4'].append(0.31)
        line_data['b']['ref_min_CD19/CD8'].append(0.53)
        line_data['b']['ref_max_CD19/CD8'].append(0.77)

        data_by_date = data[date]
        NEU = data_by_date['Нейтрофилы (NEU)']['Результат']
        LYMF = data_by_date['Лимфоциты (LYMF)']['Результат']
        CD3 = data_by_date['Общие T-лимфоциты (CD45+CD3+)']['Результат']
        CD4 = data_by_date['Т-хелперы (CD45+CD3+CD4+)']['Результат']

        line_data['b']['CD4'].append(reduce_dec_num(CD4))
        line_data['t']['CD4'].append(reduce_dec_num(CD4))

        CD8 = data_by_date['Т-цитотоксические лимфоциты (CD45+CD3+СD8+)']['Результат']

        line_data['b']['CD8'].append(reduce_dec_num(CD8))
        line_data['t']['CD8'].append(reduce_dec_num(CD8))

        CD19 = data_by_date['Общие В-лимфоциты (CD45+CD19+)']['Результат']

        line_data['b']['NEU / LYMF'].append(reduce_dec_num(NEU / LYMF))
        line_data['t']['NEU / LYMF'].append(reduce_dec_num(NEU / LYMF))

        line_data['t']['NEU / CD3'].append(reduce_dec_num(NEU / CD3))
        line_data['t']['NEU / CD4'].append(reduce_dec_num(NEU / CD4))
        line_data['t']['NEU / CD8'].append(reduce_dec_num(NEU / CD8))

        line_data['b']['LYMF / CD19'].append(reduce_dec_num(LYMF / CD19))
        line_data['b']['CD19 / CD4'].append(reduce_dec_num(CD19 / CD4))
        line_data['b']['CD19 / CD8'].append(reduce_dec_num(CD19 / CD8))

        radars_data.append({
            'b': {
                'min': [
                    9.6, 1.67, 0.53, 0.16
                ],
                'res': [
                    reduce_dec_num(LYMF / CD19),
                    reduce_dec_num(NEU / LYMF),
                    reduce_dec_num(CD19 / CD8),
                    reduce_dec_num(CD19 / CD4),
                ],
                'max':
                    [
                        10, 1.8, 0.77, 0.31
                    ],
                'names': ['LYMF/CD19', 'NEU/LYMF', 'CD19/CD8', 'CD19/CD4']
            },
            't': {
                'min':
                    [
                        2.25, 1.67, 9.47, 3
                    ],
                'res': [
                    reduce_dec_num(NEU / CD3),
                    reduce_dec_num(NEU / LYMF),
                    reduce_dec_num(NEU / CD8),
                    reduce_dec_num(NEU / CD4),
                ],
                'max':
                    [
                        3.63, 1.8, 12.3, 5
                    ],
                'names': ['NEU/CD3', 'NEU/LYMF', 'NEU/CD8', 'NEU/CD4']
            },
        })
    return name, diagnoses, dates, ages, line_data, radars_data


def make_radars_from_dic(data):
    name, diagnoses, dates, ages, line_data, radars_data = dic_prepare_data(data)
    return make_radars(radars_data[0], name, dates[0], ages[0], diagnoses[0])


def make_time_diagrams_from_dic(data):
    name, diagnoses, dates, ages, line_data, radars_data = dic_prepare_data(data)
    return make_time_diagrams(line_data, dates, name)


def save_and_close(fig, dir_path, diagram_type):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    fig.savefig("{}.png".format(dir_path, diagram_type), bbox_inches='tight')
    plt.close(fig)


def MakeSeasonDiagrams(data, rmin, rmax, season):
    fig, ax = plt.subplots(figsize=( 10,10))
    param_name = data.columns[1]
    rmin_arr = [rmin] * data.shape[0]
    rmax_arr = [rmax] * data.shape[0]

    if data.shape[0] != 0:
        ax.plot(data['Дата'], data[param_name], label = param_name, color='green', linestyle='solid')
        ax.plot(data['Дата'], rmin_arr, label = 'мин. значение нормы', color='red', linestyle='solid')
        ax.plot(data['Дата'], rmax_arr, label = 'макс. значение нормы', color='red', linestyle='solid')

    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(rotation=40)

    s = 'Весна' if season==0 else 'Осень'

    plt.title(f'Сезон: {s}', x=1.1, y=0)
    plt.subplots_adjust(left=-0.001, right=0.85, top=1, bottom=0.17)

    return fig


