import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os



def mk_plot_df(x, x_title, data, data_titles):
    df = pd.DataFrame(data=data, columns=data_titles)
    multicol2 = pd.MultiIndex.from_tuples(list(zip(['Time in ms']*len(data_titles), df.columns)))

    df = pd.DataFrame(data=df.values, columns=multicol2)
    df = df.stack(1)
    df['Metric'] = df.reset_index(0).index
    df.reset_index(drop=True, inplace=True)
    df[x_title] = np.repeat(x, len(data_titles))

    return df


def hcp_plot_data(data, plot_type, x, metric, hue, plot_name, figsize, x_scale='linear', y_scale='linear', x_min_max=None, y_min_max=None, plot_legend=True, hide_yax= False, baseline=None, palette='cool_r'):
    """
    Plot the input data to latex compatible .pgg format.
    """
    sns.set()
    sns.set_context("paper")
    if plot_type == 'bar':
        data.dropna(inplace=True, subset=[metric])
        sns.set_theme(style="whitegrid")
        sns.set_context("paper")
        g = sns.catplot(x=x, y=metric, data=data, kind=plot_type, hue=hue, ci='sd', palette=palette,
                     legend=False if plot_legend is False else True, height=figsize[1], aspect=figsize[0]/figsize[1])
        g.despine(left=True)
        if baseline is not None:
            g.map(plt.axhline, y=baseline, color='purple', linestyle='dotted')
        g.set_axis_labels(y_var=metric, x_var=x)
    else:
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
        g = sns.relplot(data=data, kind=plot_type, x=x, y=metric, hue=hue, ci='sd', palette=palette,
                     legend=plot_legend, height=figsize[1], aspect=figsize[0]/figsize[1]).set(xscale=x_scale, yscale=y_scale)
        g.despine(left=True, bottom=True)
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