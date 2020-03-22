import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#plt.rc('text', usetex=True)

#pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
#d_parser = lambda x: pd.datetime.strptime(x,'%H:%M')



# filenames = ['20030318.xls','20030319.xls','20030320.xls']
# add_on_title = ['Mòdul del vent. ', 'Direcció del vent. ', 'Flux de calor vertical. ']
# heights = ['0 m', '2.3 m', '10.5 m', '20.5 m', '35.5 m', '97.5 m']
filenames = ['20030318cov.xls','20030319cov.xls','20030320cov.xls']
add_on_title = ['Energia cinètica turbulenta. ', 'Velocitat de fricció. ', 'Flux de calor vertical. ']
heights = ['6 m', '20 m', '50 m', '100 m']

def column_name_finder (reg_exp, column_ls):
    regex = re.compile(reg_exp)
    columns = []
    names = []
    for index, name in enumerate(column_ls):
        find = type(regex.search(name))
        if find is re.Match:
            columns.append(index)
            names.append(name)
    return columns, names

label_font_s = 12
ticks_n_leg = 9
def plt_things(add_title):
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.title(add_title+title, fontsize=20)
    plt.legend(fontsize=label_font_s)
    plt.yticks(fontsize=ticks_n_leg)
    plt.tight_layout()
    plt.grid()

def parse_time (data, filename):
    month = filename[4:6]
    day = int(filename[6:8])
    time = data.columns[0]
    data[time] = [data[time][x].strftime('%H:%M') for x in range(len(data[time]))]
    for i in range(0, int(len(data[time])/2)):
        data[time][i] = str(day)+'-'+month+' '+data[time][i]
    for i in range(int(len(data[time])/2), int(len(data[time]))):
        data[time][i] = str(day+1)+'-'+month+' '+data[time][i]
    return time

data = pd.DataFrame()
title = '(CIBA, '+filenames[0][6:8]+'/'+filenames[0][4:6]+'/'+filenames[0][0:4]+'-'+\
filenames[-1][6:8]+'/'+filenames[-1][4:6]+'/'+filenames[-1][0:4]+')'
for filename in filenames:
    data0 = pd.DataFrame()

    if 'cov.xls' in filename:
        for sheet in heights:
            file = pd.read_excel('03_2003/'+filename, sheet, usecols='A:BR')
            file.columns = file.columns+' '+sheet
            data0 = pd.concat([file, data0], axis=1, sort=False)
        time = parse_time(data0,filename)
    else:
        data0 = pd.read_excel('03_2003/'+filename, usecols='A:BR')
        data0 = data0.dropna(how='any')
        time = parse_time (data0,filename)
    data = pd.concat([data,data0], axis=0, sort=False)

if 'cov.xls' in filename:
    variable_expr = ['Ecinetica', 'U\*', 'w\'t\'.*',]
    y_label = ['$E_k$ $[m^2/s^2]$', '$U^*$ $[m/s]$', '$w\'t\'$ $[K\cdot m/s]$']
else:
    variable_expr = [r'MOD.*', r'Dir.*', r'V\d+.*', r'dir\d+.*', r'T son.*']
    y_label = [r'MOD (sonic) $[m/s]$', r'Direccio (sonic) $[deg]$', r'MOD $[m/s]$', r'Direccio $[deg]$', r'Temperatura $[^oC]$']

for expr, y_lab, add_title in zip(variable_expr, y_label, add_on_title):
    columns, names = column_name_finder (expr, data.columns)
    fig, ax = plt.subplots(figsize = (13,8))
    print(names)
    for i, h in zip(names,heights):
        ax.plot(data[time][:],data[i][:], label=h)
    plt.xticks(data[time][:][::24], fontsize=ticks_n_leg,rotation=70)
    plt.ylabel(y_lab, fontsize=label_font_s)
    plt.xlabel('hora [mm-dd hh:mm]', fontsize=label_font_s)
    plt_things(add_title)
    plt.savefig('./figures/'+expr[0]+'-'+filenames[0][6:8]+'-'+filenames[-1][6:8]+'.eps')
plt.show()
