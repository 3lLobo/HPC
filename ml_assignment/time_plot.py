import matplotlib.pyplot as plt
import numpy as np
from pandas.core.arrays import base
import seaborn as sns
import pandas as pd
import os
import argparse

def plot_graph(data, plot_type,  metric, plot_name, figsize, x_min_max=None, y_min_max=None, plot_legend=True, hide_yax= False, baseline=None, palette='cool_r'):
    """
    Plot the input data to latex compatible .pgg format.
    """
    sns.set()
    sns.set_context("paper")

    if plot_type == 'bar':
        data.dropna(inplace=True, subset=[metric])
        sns.set_theme(style="whitegrid")
        g = sns.catplot(x='Workers', y=metric, data=data, kind=plot_type, hue="Model", ci='sd', palette=palette,
                     legend=False if plot_legend is False else True, height=figsize[1], aspect=figsize[0]/figsize[1])
        g.despine(left=True)
        if baseline is not None:
            g.map(plt.axhline, y=baseline, color='purple', linestyle='dotted')
        g.set_axis_labels(y_var=metric, x_var='Workers')
    else:
        g = sns.relplot(data=data, kind=plot_type, x='Workers', y=metric, hue="Model", ci='sd', palette=palette,
                     legend=plot_legend, height=figsize[1], aspect=figsize[0]/figsize[1])
        if x_min_max is not None:
            g.set(xlim=x_min_max)
    if y_min_max is not None:
        g.set(ylim=y_min_max)
    if hide_yax:
        g.set_axis_labels(y_var='')
    # plt.title(t_name.replace('_', ' ').title())
    folder = os.path.dirname(os.path.abspath(__file__)) + '/plots/'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    plt.savefig(folder + '{}_{}_{}.png'.format(plot_name, metric.replace(' ', ''), plot_type), bbox_inches='tight')
    print("Plotted " + '{}_{}_{}.png'.format(plot_name, metric.replace(' ', ''), plot_type))

if __name__ == "__main__":

#############################################################################
###################### Adjust the plot here #################################


    plot_name = 'ml_plot'
    plot_type = 'bar'       # 'bar' or 'line'
    metric = 'Test Accuracy'    # 'ETA Time' 'Train Accuracy' 'Real Time' 'Test Accuracy'
    if 'Accuracy' in metric:
        baseline = .1       # Random baseline
    else:
        baseline = None
    figsize = (4,3)
    plot_legend = False     # "auto", "brief", "full", or False
    hide_yax = False        # Hide the y axis label
    palette = 'cool_r'      #['copper_r', 'BuPu'afmhot_r cool_r] https://medium.com/@morganjonesartist/color-guide-to-seaborn-palettes-da849406d44f

#############################################################################
#############################################################################

    df_list = list()
    norm_param = {'effnet': 4.,'boring':1.6, 'resnet': 23.}

    # This loads the data if it is already saved
    if os.path.isfile('./ml_assignment/ml_results.csv'):
        df = pd.read_csv('./ml_assignment/ml_results.csv')
    else:
        for (model, model_name) in [('effnet','EfficientNet B0'), ('resnet', 'ResNet50'), ('boring', 'MyModel')]:
            for n in [1,2,4,8,11]:
                time_list = list()
                keep_falg = False
                begin_falg = True
                test_acc = np.nan
                accuracy = np.nan
                real_time = 150.
                with open("ml_assignment/results_new/hvd_out_{}_{}.txt".format(model, n),'r+') as f:
                    df = pd.DataFrame()
                    for line in f.readlines():
                        if line.split(' ')[0] == 'Epoch':
                            keep_falg = True
                            if begin_falg == True:
                                n_epochs = float(line.split('/')[1])
                                begin_falg = False
                        if keep_falg == True and 'ETA:' in line:
                            keep_falg = False
                            time_m = line.split(' - loss')[0].split(':')[1:]
                            if len(time_m) > 2:
                                time_m = float(time_m[0].strip(' ')) * 60 + float(time_m[1])
                            else:
                                time_m = float(time_m[0].strip(' '))
                            time_list.append(n_epochs * time_m)
                        accuracy = float(line.split(' - accuracy: ')[1][:6]) if " - accuracy: " in line else accuracy
                        test_acc = float(line.split('Test accuracy: ')[1]) if "Test accuracy: " in line else test_acc
                    if len(time_list) > 1:
                        time_list = time_list[1:]
                    df['Model'] = [model_name] * len(time_list)
                    df['Workers'] =  np.ones(len(time_list), dtype=int) * int(n)
                    df['ETA Time'] = np.array(time_list) #/ norm_param[model]
                    df['Train Accuracy'] = np.ones(len(time_list), dtype=float) * accuracy
                    df['Test Accuracy'] = np.ones(len(time_list), dtype=float) * test_acc
                with open("ml_assignment/results_new/hvd_err_{}_{}.txt".format(model, n),'r+') as f:
                    for line in f.readlines():
                        if 'real\t' in line:
                            real_time = float(line.split('m')[0].strip('real\t'))
                    df['Real Time'] = np.ones(len(time_list), dtype=float) * real_time
                df_list.append(df)

        df = pd.concat(df_list, axis=0)
        df.to_csv('./ml_assignment/ml_results.csv')
        print('Saved data in ml_results.csv')

    x_min_max = (1, max(df['Workers']))
    y_min_max = (0, max(df[metric])) #if max(df[metric])< 250 else 250)
    if 'Accuracy' in metric:
        y_min_max = (0, 1)
    plot_graph(df, plot_type, metric, plot_name, figsize, x_min_max, y_min_max, plot_legend, hide_yax, baseline, palette)
