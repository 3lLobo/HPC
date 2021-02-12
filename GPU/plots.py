import pandas as pd
import sys,os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from plot_sns import hcp_plot_data, mk_plot_df


#############################################################################
###################### Adjust the plot here #################################


plot_name = 'gpu_plot'
plot_type = 'line'       # 'bar' or 'line'
figsize_single = (6,3)
figsize_two = (4,3)
plot_legend = False     # "auto", "brief", "full", or False
hide_yax = False        # Hide the y axis label
palette = 'cool_r'      #['copper_r', 'BuPu'afmhot_r cool_r] https://medium.com/@morganjonesartist/color-guide-to-seaborn-palettes-da849406d44f

#############################################################################
#############################################################################

# EXERCISE 1B
df = pd.DataFrame()


df['Sequential time'] = yseq = np.array([0.000000409412,0.00000129765,0.000280118,0.00199624,0.00322239])*1000
df['Kernel time'] = yker = np.array([0.0000258153,0.0000148906,0.0000290765,0.0000685247,0.000111429])*1000
df['Memory time'] = ymem = np.array([0.0000677165,0.0000316824,0.000493309,0.00468201,0.0047436])*1000
df['Kernel + Memory time'] = df['Kernel time'] + df['Memory time']

x = np.repeat([256,1024,65536,655360,1000000], 1)

df_1 = mk_plot_df(x, 'Array Length', df.values, df.columns)

hcp_plot_data(df_1, plot_type, 'Array Length', 'Time in ms','Metric', plot_name+'1b', figsize_single, 'log', 'log', x_min_max=(min(df_1['Array Length']),max(df_1['Array Length'])), y_min_max=(0,max(df_1['Time in ms'])), plot_legend=True, hide_yax= False)

# EXERCISE 1C
data_title = ['Sequential time', 'Kernel time', 'Memory time', 'Kernel + Memory time']
x = np.repeat([256,1024,65536,655360,1000000], 1)
df = pd.DataFrame()
df['Sequential time'] = [0.0016987,0.00294081,0.00103352,0.0010219,0.00101749]
df['Kernel time'] = [0.0000687494,0.0000670506,0.0000708141,0.0000652788,0.0000692318]
df['Memory time'] = [0.00449514,0.00443542,0.00216878,0.00215384,0.0021569]
df['Kernel + Memory time'] = df['Kernel time'] + df['Memory time']

df = mk_plot_df(x, 'Array Length', df.values, df.columns)

hcp_plot_data(df, plot_type, 'Array Length', 'Time in ms','Metric', plot_name+'1c', figsize_single, 'log', y_scale='linear', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= False)

# EXERCISE 1D

# N = 4
# ind = np.arange(N)  # the x locations for the groups
# width = 0.2       # the width of the bars

# fig = plt.figure()
# ax = fig.add_subplot(111)

yseq = [0.00209373,0.00295677,0.00102963,0.00119784]
# rects1 = ax.bar(ind, yseq, width, color='r')
yker = [0.0000732894,0.0000735553,0.0000737247,0.0000757035]
# rects2 = ax.bar(ind+width, yker, width, color='g')
ymem = [0.00453237,0.00311698,0.00216885,0.00217114]
# rects3 = ax.bar(ind+width*2, ymem, width, color='b')
# ytot = []
# for i in range(0,4):
#     ytot.append(yker[i]+ymem[i])
# rects4 = ax.bar(ind+width*3,ytot,width,color='y')

# ax.set_ylabel('Time in seconds')
# ax.set_xticks(ind+width)
# ax.set_xticklabels( ('Addition', 'Subtraction', 'Multiplication', 'Division') )
# ax.legend( (rects1[0], rects2[0], rects3[0],rects4[0]), ('Sequential time', 'Kernel time', 'Memory time', 'Kernel time + Memory time') )
# plt.title('Time for vector addition, substraction, multiplication and division')
# plt.show()

op_names = ['Addition', 'Subtraction', 'Multiplication', 'Division']
x_dict =  dict((x,y) for x, y in list(zip(np.arange(len(data_title)), data_title)))
df = mk_plot_df(np.arange(len(data_title)), 'x', [yseq, yker, ymem, np.add(yker, ymem)], op_names)
df['Operator'] = df['Metric']
x_names = []
for n in df['x']:
    x_names.append(x_dict[n])
df['Metric'] = x_names
hcp_plot_data(df, 'bar', 'Operator', 'Time in ms','Metric', plot_name+'1d', figsize_single, 'log', y_scale='linear', x_min_max=None, y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= False)

# break
#EXERCISE 1E events REACTION Left

x = [65536,655360,1000000]
yadd = [0.006784,0.022368,0.039872]
ysub = [0.010144,0.027488,0.039008]
ymul = [0.011104,0.02816,0.038944]
ydiv = [0.009152,0.023616,0.041664]

# fig, ax = plt.subplots()
# ax.plot(x,yadd,label='Vector addition')
# ax.plot(x,ysub,label='Vector subtraction')
# ax.plot(x,ymul,label='Vector multiplication')
# ax.plot(x,ydiv,label='Vector division')
# legend = ax.legend()
# plt.xticks(x)
# plt.xlabel('Array length')
# plt.ylabel('Time in milliseconds')
# plt.title('Time for different vector operations for different array sizes')
# plt.show()

# x_dict =  dict((x,y) for x, y in list(zip(np.arange(len(data_title)), data_title)))
df = mk_plot_df(np.array(x), 'Array Length',np.array([yadd, ysub, ymul, ydiv]).T,['Addition', 'Subtraction', 'Multiplication', 'Division'])
df['Operator'] = df['Metric']
# x_names = []
# for n in df1d['x']:
#     x_names.append(x_dict[n])
# df1d['Metric'] = x_names
hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Operator', plot_name+'1e_react', figsize_two, 'log', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=False, hide_yax= False)


# EXERCISE 1E normal Computation

yadd = np.array([0.0000361365,0.0000678824,0.000105817]) * 1000
ysub = np.array([0.0000343683,0.0000683059,0.000104384]) * 1000
ymul = np.array([0.0000360718,0.0000678447,0.000104834]) * 1000
ydiv = np.array([0.0000335212,0.0000701953,0.000107264]) * 1000

# fig, ax = plt.subplots()
# ax.plot(x,yadd,label='Vector addition')
# ax.plot(x,ysub,label='Vector subtraction')
# ax.plot(x,ymul,label='Vector multiplication')
# ax.plot(x,ydiv,label='Vector division')
# legend = ax.legend()
# plt.xticks(x)
# plt.xlabel('Array length')
# plt.ylabel('Time in seconds')
# plt.title('Time for different vector operations for different array sizes')
# plt.show()

df = mk_plot_df(np.array(x), 'Array Length', np.array([yadd, ysub, ymul, ydiv]).T,['Addition', 'Subtraction', 'Multiplication', 'Division'])
df['Operator'] = df['Metric']

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Operator', plot_name+'1e_comp', figsize_two, 'log', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= True)


# EXERCISE 2 

x = [256,1024,65536,655360,1000000]
yseq = [0.00000353294,0.00000623059,0.000388667,0.0060765,0.00660711]
yker = [0.0000267106,0.0000153576,0.00003178,0.0000715365,0.000111222]
ymem = [0.0000644847,0.000040159,0.000409668,0.00274454,0.00431247]
ytot = []
for i in range(0,5):
    ytot.append(yker[i]+ymem[i])

# fig, ax = plt.subplots()
# ax.plot(x,yseq,label='Sequential time')
# ax.plot(x,yker,label = 'Kernel time')
# ax.plot(x,ymem,label = 'Memory time')
# ax.plot(x,ytot,label = 'Kernel time + Memory time')
# legend = ax.legend()
# plt.xticks(x)
# plt.xlabel('Array length')
# plt.ylabel('Time in seconds')
# plt.title('Time for vector transformation for different array sizes')
# plt.show()


df = mk_plot_df(np.array(x), 'Array Length', np.array([yseq, yker, ymem, ytot,]).T, data_title)

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Metric', plot_name+'2', figsize_single, 'log', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= False)


# EXERCISE 3 ENCRYPTION

x = [5947,67154,93318,466867,577751]
yseq = [0.000097,0.001257,0.001162,0.005941,0.004403]
yker = [0.000046,0.000052,0.000022,0.000133,0.000066]
ymem = [0.000093,0.000219,0.000097,0.000592,0.000385]
ytot = []
for i in range(0,5):
    ytot.append(yker[i]+ymem[i])

# fig, ax = plt.subplots()
# ax.plot(x,yseq,label='Sequential time')
# ax.plot(x,yker,label = 'Kernel time')
# ax.plot(x,ymem,label = 'Memory time')
# ax.plot(x,ytot,label = 'Kernel time + Memory time')
# legend = ax.legend()
# plt.xlabel('File size')
# plt.ylabel('Time in seconds')
# plt.title('Time for encryption for different text sizes')
# plt.show()

df = mk_plot_df(np.array(x), 'Array Length', np.array([yseq, yker, ymem, ytot,]).T, data_title)
# df['Operator'] = df['Metric']

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Metric', plot_name+'3encrypt', figsize_two, 'linear', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=False, hide_yax= False)


# EXERCISE 3 DECRYPTION

x = [5947,67154,93318,466867,577751]
yseq = [0.000075,0.000802,0.000544,0.004880,0.003616]
yker = [0.000038,0.000048,0.000025,0.000102,0.000063]
ymem = [0.000065,0.000143,0.000091,0.000513,0.000327]
ytot = []
for i in range(0,5):
    ytot.append(yker[i]+ymem[i])

# fig, ax = plt.subplots()
# ax.plot(x,yseq,label='Sequential time')
# ax.plot(x,yker,label = 'Kernel time')
# ax.plot(x,ymem,label = 'Memory time')
# ax.plot(x,ytot,label = 'Kernel time + Memory time')
# legend = ax.legend()
# plt.xlabel('File size')
# plt.ylabel('Time in seconds')
# plt.title('Time for decryption for different text sizes')
# plt.show()

df = mk_plot_df(np.array(x), 'Array Length', np.array([yseq, yker, ymem, ytot,]).T, data_title)
# df['Operator'] = df['Metric']

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Metric', plot_name+'3decrypt', figsize_two, 'linear', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= True)


# EXERCISE 4 ENCRYPTION

x = [5947,67154,93318,466867,577751]
yseq = [0.0000318,0.003863,0.003552,0.021573,0.034481]
yker = [0.000044,0.000054,0.000058,0.000160,0.000272]
ymem = [0.0000114,0.000189,0.000232,0.000687,0.000834]
ytot = []
for i in range(0,5):
    ytot.append(yker[i]+ymem[i])

# fig, ax = plt.subplots()
# ax.plot(x,yseq,label='Sequential time')
# ax.plot(x,yker,label = 'Kernel time')
# ax.plot(x,ymem,label = 'Memory time')
# ax.plot(x,ytot,label = 'Kernel time + Memory time')
# legend = ax.legend()
# plt.xlabel('File size')
# plt.ylabel('Time in seconds')
# plt.title('Time for encryption for different text sizes')
# plt.show()


df = mk_plot_df(np.array(x), 'Array Length', np.array([yseq, yker, ymem, ytot,]).T, data_title)
# df['Operator'] = df['Metric']

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Metric', plot_name+'4encrypt', figsize_two, 'linear', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=False, hide_yax= False)



# EXERCISE 4 DECRYPTION

x = [5947,67154,93318,466867,577751]
yseq = [0.000245,0.002702,0.0003806,0.018418,0.023714]
yker = [0.000035,0.000044,0.000047,0.000166,0.000217]
ymem = [0.000069,0.000155,0.000189,0.000590,0.000721]
ytot = []
for i in range(0,5):
    ytot.append(yker[i]+ymem[i])

# fig, ax = plt.subplots()
# ax.plot(x,yseq,label='Sequential time')
# ax.plot(x,yker,label = 'Kernel time')
# ax.plot(x,ymem,label = 'Memory time')
# ax.plot(x,ytot,label = 'Kernel time + Memory time')
# legend = ax.legend()
# plt.xlabel('File size')
# plt.ylabel('Time in seconds')
# plt.title('Time for decryption for different text sizes')
# plt.show()


df = mk_plot_df(np.array(x), 'Array Length', np.array([yseq, yker, ymem, ytot,]).T, data_title)
# df['Operator'] = df['Metric']

hcp_plot_data(df, 'line', 'Array Length', 'Time in ms', 'Metric', plot_name+'4decrypt', figsize_two, 'linear', y_scale='log', x_min_max=(min(df['Array Length']),max(df['Array Length'])), y_min_max=(0,max(df['Time in ms'])), plot_legend=True, hide_yax= True)
