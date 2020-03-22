
import re
import datetime
import numpy as npZ
import pandas as pd
import matplotlib.pyplot as plt

#plt.rc('text', usetex=True)

#pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
#d_parser = lambda x: pd.datetime.strptime(x,'%H:%M')

# filenames = ['20030318.xls','20030319.xls','20030320.xls']
filenames = ['20030318cov.xls','20030319cov.xls','20030320cov.xls']
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
def plt_things():
    plt.title(title, fontsize=20)
    plt.legend(fontsize=label_font_s)
    ax.xaxis.set_major_locator(plt.MaxNLocator(30))
    plt.xticks(fontsize=ticks_n_leg,rotation=70)
    plt.yticks(fontsize=ticks_n_leg)
    plt.tight_layout()
    plt.grid()

def parse_time (data, filename):
    time = data.columns[0]
    data[time] = [data[time][x].strftime('%H:%M') for x in range(len(data[time]))]
    data[time] = filename[6:8]+'/'+filename[4:6]+' '+data[time][:]
    return time


for filename in filenames:
    data = pd.DataFrame()
    title = 'CIBA, '+filename[6:8]+'/'+filename[4:6]+'/'+filename[0:4]

    if 'cov.xls' in filename:
        for sheet in heights:
            file = pd.read_excel('03_2003/'+filename, sheet, usecols='A:BR')
            file.columns = file.columns+' '+sheet
            data = pd.concat([file, data], axis=1, sort=False)
        time = parse_time(data,filename)
    else:
        data = pd.read_excel('03_2003/'+filename, usecols='A:BR')
        data = data.dropna(how='any')
        time = parse_time (data,filename)


    if 'cov.xls' in filename:
        variable_expr = ['Ecinetica', 'U\*', 'w\'t\'.*',]
        y_label = ['$E_k$', '$U^*$', '$w\'t\'[K\cdot m/s]$']
    else:
        variable_expr = [r'MOD.*', r'Dir.*', r'V\d+.*', r'dir\d+.*', r'T son.*']
        y_label = [r'MOD (sonic) $[m/s]$', r'Direccio (sonic) $[deg]$', r'MOD $[m/s]$', r'Direccio $[deg]$', r'Temperatura $[^oC]$']

    for expr, y_lab in zip(variable_expr, y_label):
        columns, names = column_name_finder (expr, data.columns)
        fig, ax = plt.subplots(figsize = (13,8))
        print(names)
        for i in names:
            ax.plot(data[time][:],data[i][:], label=i)
        plt.ylabel(y_lab, fontsize=label_font_s)
        plt.xlabel('hora [mm-dd hh:mm]', fontsize=label_font_s)
        plt_things()
        plt.savefig('./figures/'+expr[:4]+'_'+filename+'.eps')
        #plt.show()
