import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt

# Close everything
plt.close('all')

# Save figures in high res
save_fig = True

# Format specifiers
#-----------------------------------------
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')

# Presentations
plt.rcParams.update({
    "text.usetex": True,
    "figure.figsize": (10,10),
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 30,
    "font.weight": "bold",
    "lines.linewidth": 2,
    "lines.markeredgewidth": 2.0,
    "lines.markersize": 12,
    "axes.titlesize": 36,
    "axes.labelsize": 36,
    "axes.linewidth": 3.0,
    "xtick.major.width": 3.0,
    "xtick.minor.width": 1.0,
    "xtick.major.size": 3.0,
    "xtick.minor.size": 1.0,
    "xtick.direction": "in",
    "ytick.major.width": 3.0,
    "ytick.minor.width": 1.0,
    "ytick.major.size": 3.0,
    "ytick.minor.size": 1.0,
    "ytick.direction": "in",
    "legend.fontsize": 28,
})

# Load WRF data
#-----------------------------------------
nx_WRF = 1500
nt_WRF = 4
print("Loading WRF data...")
data = np.load('WRF_Rain_Accum_3000_6000_9000.npz')

# Load the ERF data
#-----------------------------------------
nx_ERF = 1001
nt_ERF = 4
x_ERF  = np.empty(shape=(nx_ERF,nt_ERF)) 
rain_accum_ERF = np.empty(shape=(nx_ERF,nt_ERF))
time = np.array([0, 3000.0, 6000.0, 9000.0])

print("Loading ERF data...")
t = 0
with open('Rain_accum_0.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  cnt = -1
  for lines in csvFile:
    if (cnt==-1):
      print("Header: ",lines)
    else:
      x_ERF[cnt,t] = float(lines[1])
      rain_accum_ERF[cnt,t] = float(lines[0])

    cnt += 1
      

t = 1
with open('Rain_accum_3000.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  cnt = -1
  for lines in csvFile:
    if (cnt==-1):
      print("Header: ",lines)
    else:
      x_ERF[cnt,t] = float(lines[1])
      rain_accum_ERF[cnt,t] = float(lines[0])

    cnt += 1

t = 2
with open('Rain_accum_6000.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  cnt = -1
  for lines in csvFile:
    if (cnt==-1):
      print("Header: ",lines)
    else:
      x_ERF[cnt,t] = float(lines[1])
      rain_accum_ERF[cnt,t] = float(lines[0])

    cnt += 1

t = 3
with open('Rain_accum_9000.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  cnt = -1
  for lines in csvFile:
    if (cnt==-1):
      print("Header: ",lines)
    else:
      x_ERF[cnt,t] = float(lines[1])
      rain_accum_ERF[cnt,t] = float(lines[0])

    cnt += 1

# Plot the data
#-----------------------------------------
# Color by time if we want each instance
colors_ERF = plt.cm.Blues(np.linspace(0.2, 0.8, nt_ERF))

plt.figure()

for i in range(1,nt_WRF):
    plt.plot((data['x'][::4]-75000.0)/1000.0, data['rain_accum'][::4,i], \
             ls='none', color=colors_ERF[i], \
             marker='.', mfc='w', \
             label='_nolegend_')
    
for i in range(1,nt_ERF):
    plt.plot((x_ERF[:,i]-75000.0)/1000.0, rain_accum_ERF[:,i], \
             ls='-', color=colors_ERF[i], \
             marker='None', mfc='w', \
             label=r"$t =$" + str(time[i]) + " [s]")


plt.xlabel(r"$x$ [km]")
plt.ylabel(r"$h$ [mm]",)
plt.legend(loc="upper right", frameon=False)
plt.xticks(np.linspace(-30.0, 30.0, num=7))
plt.yticks(np.linspace(0.0, 180.0, num=10))

# Square axis & padding for labels
ax = plt.gca()
ax.set_xlim([-30.0, 30.0])
ax.set_ylim([-1.0, 180.0])
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.tight_layout()
plt.grid(True, linestyle=':',alpha=0.75)
if (save_fig):
    plt.savefig("Squall_Line_Rain_Accum.png",dpi=300,bbox_inches='tight')
plt.show()


