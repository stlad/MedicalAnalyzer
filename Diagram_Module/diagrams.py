import json, math, os
from copy import copy

import numpy as np
import pylab as pl
from matplotlib import pyplot as plt


def reduce_dec_num(val):
    return math.ceil(val * 10) / 10

class Radar(object):

    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            # rect = [0.05, 0.05, 0.95, 0.95]
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


def make_radar_diagram(data, output_dir, date, file_name):
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
    pl.title(file_name, pad=30)
    #plt.show()

    #fig.savefig("{}\\{}\\{}.png".format(output_dir, date, file_name), bbox_inches='tight')
    return  fig

def make_radars(data, date, output_dir):
    make_radar_diagram(
        data['b'],
        output_dir,
        date,
        'Показатели В - клеточного звена иммунитета')
    make_radar_diagram(
        data['t'],
        output_dir,
        date,
        'Показатели T - клеточного звена иммунитета')

def get_radars(data, date, output_dir):
    b_diag = make_radar_diagram(
        data['b'],
        output_dir,
        date,
        'Показатели В - клеточного звена иммунитета')
    t_diag = make_radar_diagram(
        data['t'],
        output_dir,
        date,
        'Показатели T - клеточного звена иммунитета')

    return (b_diag, t_diag)


def make_time_diagram(arr, dates, labels, path, name):
    fig, ax = plt.subplots()
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    for i in range(arr):
        marker = '-'
        if i % 3 >= 1:
            marker = '--'
        ax.plot(dates, arr[i], label=labels[i], color=colors[i // 3], marker=marker)
    ax.legend()
    plt.savefig('{}\\{}.png'.format(path, name))


def prepare_data(data):
    data_keys = list(data.keys())
    name = data_keys[0]
    data = data[name]
    dates = copy(list(data.keys()))
    line_data = {
        't': {
            'ref_min_CD8': [],
            'ref_max_CD8': [],
            'ref_min_CD4': [],
            'ref_max_CD4': [],
            'ref_min_NEU/LYMF': [],
            'ref_max_NEU/LYMF': [],
            'ref_min_NEU/CD3': [],
            'ref_max_NEU/CD3': [],
            'ref_min_NEU/CD4': [],
            'ref_max_NEU/CD4': [],
            'ref_min_NEU/CD8': [],
            'ref_max_NEU/CD8': [],
            'CD8': [],
            'CD4': [],
            'NEU / LYMF': [],
            'NEU / CD3': [],
            'NEU / CD4': [],
            'NEU / CD8': [],
        },
        'b': {
            'ref_min_CD8': [],
            'ref_max_CD8': [],
            'ref_min_CD4': [],
            'ref_max_CD4': [],
            'ref_min_NEU/LYMF': [],
            'ref_max_NEU/LYMF': [],
            'ref_min_LYMF/CD19': [],
            'ref_max_LYMF/CD19': [],
            'ref_min_CD19/CD4': [],
            'ref_max_CD19/CD4': [],
            'ref_min_CD19/CD8': [],
            'ref_max_CD19/CD8': [],
            'CD8': [],
            'CD4': [],
            'NEU / LYMF': [],
            'LYMF / CD19': [],
            'CD19 / CD4': [],
            'CD19 / CD8': [],
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
                    9.6, 1.67, 0.31, 0.16
                ],
                'res': [
                    reduce_dec_num(LYMF / CD19),
                    reduce_dec_num(NEU / LYMF),
                    reduce_dec_num(CD19 / CD8),
                    reduce_dec_num(CD19 / CD4),
                ],
                'max':
                    [
                        10, 1.8, 0.53, 0.77
                    ],
                'names': ['LYMF/CD19', 'NEU/LYMF', 'CD19/CD8', 'CD19/CD4']
            },
            't': {
                'min':
                    [
                        2.25, 1.67, 3, 5
                    ],
                'res': [
                    reduce_dec_num(NEU / CD3),
                    reduce_dec_num(NEU / LYMF),
                    reduce_dec_num(NEU / CD8),
                    reduce_dec_num(NEU / CD4),
                ],
                'max':
                    [
                        3.63, 1.8, 12.3, 9.47
                    ],
                'names': ['NEU/CD3', 'NEU/LYMF', 'NEU/CD8', 'NEU/CD4']
            },
        })
    return name, dates, line_data, radars_data


def make_time_diagrams(data, dates, path):
    keys = copy(data['t'].keys())
    arr = []
    for key in keys:
        arr.append(data['t'][key])
    make_time_diagram(arr, dates, keys, path, 'Т-клеточное звено')
    keys = copy(data['b'].keys())
    arr = []
    for key in keys:
        arr.append(data['b'][key])
    make_time_diagram(arr, dates, keys, path, 'B-клеточное звено')

def smth():
#if __name__ == "__main__":
    path = "C:\\Users\\edvso\\PycharmProjects\\HelthProject"
    json_name = "data"
    name, dates, line_data, radars_data = prepare_data("{}\\{}.json".format(path, json_name))
    for i in range(len(radars_data)):
        make_radars(radars_data[i], dates[i], "{}\\{}".format(path, name))
    make_time_diagrams(line_data, dates, "{}\\{}".format(path, name))
