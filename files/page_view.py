'''
created by Paolo
August 11, 2021
'''

import pandas as pd
import matplotlib.pyplot as plt
fontSz = 15
fontsz = 20
fontssz = 11
# clr = ['maroon', 'lightcoral'] 
clr = ['maroon', 'orangered', 'lightcoral', 'gold']
clr = ['maroon', 'orangered', 'gold', 'white']
# clr = ['b', 'g', 'r', 'c']#, 'm']

file = '/Users/paolocremonese/Downloads/data-export.csv'

cf = pd.read_csv(file, sep=',', index_col=0, comment='#')
cff = pd.read_csv(file, sep=',', index_col=0, comment='#')
# print(cf.head())

cd = open(file, "r")
scd = cd.read()
ii = scd.find("Data di inizio")+16

di = pd.to_datetime(scd[ii:ii+8])
dt = pd.Timedelta(1, 'D')
dates = [di+(dt*i) for i in cf.index]

ida = pd.to_datetime('20210610')
fda = pd.to_datetime('20210810')

for n,i in enumerate(dates):
     if i==ida:
         ii = n
     if i==fda:
         fi = n
'''
ii = 0
fi = len(dates)
# '''

# mean
'''
for n,i in enumerate(cf.columns):
    for x in range(1, len(cf[i])-1):
       cf[i][x] = (cff[i][x-1]+cff[i][x]+cff[i][x+1])/2
'''
# plot

plt.figure(figsize=(16,9))

for n,i in enumerate(cf.columns[:-1]):
    ln = 20 - len(i)
    ln = [5, 30, 24, 27]
    lab = ' '*ln[n] + ' %i'%(sum(cf[i][ii:fi]))
    plt.plot(dates[ii:fi], cf[i][ii:fi], label=i+lab, c=clr[n])

'''
plt.plot(dates, cf[cf.columns[-1]], c=clr[-1], label='blog Mexico')
# '''
plt.xticks(rotation=20)
plt.tick_params(axis='both',which='both',direction='out',labelsize=fontsz)

# plt.xlabel('Dates', fontsize=fontsz)
plt.ylabel('visit #', fontsize=fontsz)

plt.legend(loc=9, fontsize=fontsz, framealpha=0.)  #title="page name", title_fontsize='xx-large',
# plt.legend(ncol=3,loc='upper center',bbox_to_anchor=(0.5,1.15),fontsize=fontsz,framealpha=0.)

path_fig = '/Users/paolocremonese/Dropbox/PhD/html/web-page/images/page_view.jpg'
plt.savefig(path_fig, dpi=300, format='png', bbox_inches="tight", transparent=True)
plt.close()
