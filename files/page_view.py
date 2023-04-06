'''
created by Paolo
August 11, 2021
'''
import os
import sys
path_home = os.path.expanduser('~')
import pandas as pd
import matplotlib.pyplot as plt
'''
if 'paolocremonese' in path_home:
    sys.path.insert(1, '/Library/TeX/texbin')

# to use LaTex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
'''
fontSz = 15
fontsz = 20 #13
fontssz = 11
# clr = ['maroon', 'lightcoral'] 
clr = ['maroon', 'orangered', 'lightcoral', 'gold']
clr = ['maroon', 'orangered', 'gold', 'white', 'chocolate']
columns = ['Paolo Cremonese', 'CV', 'Album', 'Blog', 'Extras']
# clr = ['b', 'g', 'r', 'c']#, 'm']

file = path_home + '/Downloads/data-export.csv'
# file = '/Users/paolocremonese/Downloads/data-export-2.csv'

cf = pd.read_csv(file, sep=',', index_col=0, comment='#', skiprows=range(103,125))
cff = pd.read_csv(file, sep=',', index_col=0, comment='#', skiprows=range(103,150))
# print(cf.head())

cd = open(file, "r")
scd = cd.read()
ii = scd.find("Data di inizio")+16

di = pd.to_datetime(scd[ii:ii+8])
dt = pd.Timedelta(1, 'D')
dates = [di+(dt*i) for i in cf.index]

# [print(i) for i in dates]

#%% for 3 months period
ida = pd.to_datetime('2023-01-04')
fda = pd.to_datetime('2023-04-03')

for n,i in enumerate(dates):
     if i==ida:
         ii = n
     if i==fda:
         fi = n+1

# plot

fig = plt.figure(figsize=(16,9))

# for n,i in enumerate(cf.columns):
for n,i in enumerate(columns):
    visits = str(sum(cf[i][ii:fi]))
    ls = len(i)
    li = len(visits)
    ns = 20-ls-li
    # print(ns)
    lab = '%s'%(i)+' '*ns + ' %s'%(visits)
    if i == "Paolo Cremonese" or i == "CV":
        lw = 2
    else:
        lw = 1
    plt.plot(dates[ii:fi], cf[i][ii:fi], label=lab, c=clr[n], linewidth=lw)

plt.xticks(rotation=20)
plt.tick_params(axis='both',which='both',direction='out',labelsize=fontsz)

plt.ylabel('visit #', fontsize=fontsz)

ax = fig.get_axes()[0]
legend = ax.legend(framealpha=0., prop={'family': 'monospace', 'size':fontsz})  #title="page name", title_fontsize='xx-large', loc=9 loc='upper center', 

# path_fig = path_home+'/Dropbox/PhD/html/web-page/images/page_view.jpg'
path_fig = path_home+'/Documents/git/PaoloCremo.github.io/images/page_view.jpg'
#'''
plt.savefig(path_fig, dpi=300, format='png', bbox_inches="tight", transparent=True)
plt.close()
'''
plt.show()
# '''

# sys.exit(0)

######################
## for single month ##
######################

months = ['January', 'February', 'March']
mn = '02'
month = months[int(mn)-1] 
ida = pd.to_datetime('2023-'+mn+'-01')
fda = pd.to_datetime('2023-'+mn+'-31')

for n,i in enumerate(dates):
     if i==ida:
         ii = n
     if i==fda:
         fi = n+1
'''
ii = 0
fi = len(dates)
# '''

# plot

plt.figure()
plt.title(month+', 2022')


for n,i in enumerate(columns):

    visits = str(sum(cf[i][ii:fi]))
    ls = len(i)
    li = len(visits)
    ns = 18-ls-li
    # print(ns)
    lab = '%s'%(i)+' '*ns + ' %s'%(visits)
    if i == "Paolo Cremonese" or i == "CV":
        lw = 2
    else:
        lw = 1
    plt.plot([dx.day for dx in dates[ii:fi]], cf[i][ii:fi], label=lab, c=clr[n])

plt.ylim(-0.4, 10.5)

'''
plt.plot([dx.day for dx in dates[ii:fi]], cf[cf.columns[0]], c='k', label='tot  %i '%(sum(cf[cf.columns[0]])))
# '''
plt.tick_params(axis='both',which='both',direction='out',labelsize=fontssz)

plt.ylabel('visit #', fontsize=fontssz)

plt.legend(framealpha=0., prop={'family': 'monospace', 'size':fontssz})#, loc='upper center')  #title="page name", title_fontsize='xx-large', loc=9
'''
shift = max([t.get_window_extent().width for t in legend.get_texts()])
for t in legend.get_texts():
    t.set_ha('right') # ha is alias for horizontalalignment
    t.set_position((shift,0))
'''    

#plt.legend(fontsize=fontssz, framealpha=0., loc='upper left')  # month
# plt.legend(ncol=3,loc='upper center',bbox_to_anchor=(0.5,1.15),fontsize=fontsz,framealpha=0.)

# path_fig = path_home+'/Dropbox/PhD/html/web-page/images/page_view_22'+mn+'.jpg'
path_fig = path_home+'/Documents/git/PaoloCremo.github.io/images/page_view_23'+mn+'.jpg'

plt.savefig(path_fig, dpi=300, format='png', bbox_inches="tight", transparent=True)
plt.close()
