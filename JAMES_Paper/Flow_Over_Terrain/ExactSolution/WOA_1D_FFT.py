import math
import cmath
import numpy as np
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy.fft import fft, dst, ifft, idst, fftfreq

plt.rcParams.update({
    "text.usetex": True,
    "figure.figsize": (10,10),
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 32,
    "font.weight": "bold",
    "lines.linewidth": 2,
    "lines.markeredgewidth": 2.0,
    "lines.markersize": 10,
    "axes.titlesize": 32,
    "axes.labelsize": 34,
    "axes.linewidth": 2.5,
    "xtick.major.width": 2.5,
    "xtick.minor.width": 2.0,
    "ytick.major.width": 2.5,
    "ytick.minor.width": 2.0,
    "legend.fontsize": 26,
})

plt.close('all')


# Analytical functions
#==================================================
# Mountain deformation
def height (hm, a, x, xc) :
    r2  = ((x-xc) / a )**2.0
    sol = hm / (1.0 + r2)
    return sol

# Stratificaton
def N_freq() :
    return (0.010)

# Density
def rho(z) :
    T0    = 300.0
    p00   = 1e5
    g     = 9.80616
    cp    = 1004.67
    rgas  = 287.17
    cv    = cp-rgas
    gamma = cp/cv
    xappa = rgas/cp

    N2    = N_freq()**2.0
    delta = 1.0 - (g**2.0)/(cp*N2*T0)
    expi  = np.exp(-N2/g*z) + delta*(1.0 - np.exp(-N2/g*z))
    theta = T0*np.exp(N2/g*z)
    T     = expi*theta
    p     = p00*(expi**(gamma/(gamma-1.0)))
    rho   = p/(rgas*T)
    return (rho)

# Simulation conditions
#==================================================

# Reference solution points
df = pd.read_csv("GR08_soln.csv")
#print(df)
#print(df.dtypes)
#print(df["60.30371077002231"].to_numpy())
#print(df[" 9.163113459669589"].to_numpy())
#exit()
XGR = (df["60.30371077002231"].to_numpy() - 72.0) * 1000.0
YGR = df[" 9.163113459669589"].to_numpy() * 1000.0

# Spectral coeff number
N1 = 2048
N3 = 1024

# Hill parameters
hmax = 1.0
aval = 1000.0
Uin  = 10.0

# Domain size
xmax = 100*aval
xmin = -xmax
zmax = 12000.0
zmin = 0.0

# ETA solution meshgrid
x     = np.linspace(xmin, xmax, N1)
z     = np.linspace(zmin, zmax, N3)
eta   = np.zeros(N1,dtype=np.complex_)
reta  = np.zeros(N1)
retao = np.zeros(N1)
dx = x[1] - x[0]
dz = z[1] - z[0]

# Wp solution meshgrid
xp = np.zeros(N1-1)
wp = np.zeros((N3,N1-1))
for k in range(N1-1) :
    xp[k] = 0.5 * (x[k+1] + x[k])
X2, Z2 = np.meshgrid(xp,z)

# Up solution meshgrid
zp = np.zeros(N3-1)
up = np.zeros((N3-1,N1))
for k in range(N3-1) :
    zp[k] = 0.5 * (z[k+1] + z[k])
X3, Z3 = np.meshgrid(x,zp)
dz2 = zp[1] - zp[0]

# Wave numbers
kwave = 2.0 * np.pi * fftfreq(N1, d=dx)

print("Zmax = " ,zmax)
print("N    = ",N_freq())
print("Na/U = ",N_freq()*aval/Uin)
print("dx   = ",dx)
print("dz   = ",dz)
print("Ratio of grid to hill width: ",aval/dx)


# Forward transform the bottom BC
#--------------------------------------------------
hxy = np.zeros(N1)
for k in range(N1) :
    hxy[k] = height(hmax, aval, x[k], 0.0)
HKL = fft(hxy)


# Construct the solution on z planes
#--------------------------------------------------
for nz in range(N3) :
    for k in range(N1) :
        kw = kwave[k]

        # Select the desired root
        m2 = (N_freq() / Uin)**2.0 - kw**2.0
        m  = cmath.sqrt(m2)
        ms = complex(0.0,0.0)
        if (m2 < 0.0) :                        # only imaginary root
            ms = complex(0.0,abs(np.imag(m)))
        else :                                 # only real root
            if (np.sign(kw) != np.sign(np.real(m))) :
                ms = complex(-np.real(m),0.0)
            else :
                ms = complex( np.real(m),0.0)

        # Pointwise multiplication of ODE solution
        eta[k] = HKL[k] * np.exp(1j * ms * z[nz])


    # Inverse transform to physical domain
    #--------------------------------------------------
    fc   = np.sqrt( rho(0.0)/rho(z[nz]) )
    reta = fc*np.real(ifft(eta))


    # w solution
    #--------------------------------------------------
    for k in range(N1-1) :
        wp[nz,k] = Uin * (reta[k+1] - reta[k]) / dx


    # u solution
    #--------------------------------------------------
    if (nz>0) :
        for k in range(N1) :
            up[nz-1,k] = -Uin * (reta[k] - retao[k]) / dz


    # Transfer solution to old
    #--------------------------------------------------
    retao[:] = reta[:]


# Write data to VTK
#==================================================
with open("WOA_1D_Analytical_w.vtk", "w") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("2D data\n")
    f.write("ASCII\n")
    f.write("DATASET STRUCTURED_GRID\n")
    f.write(f"DIMENSIONS {N1-1} 1 {N3}\n")
    f.write("POINTS {} float\n".format((N1-1) * N3))
    for k in range(N3):
        for i in range(N1-1):
            f.write(f"{X2[k,i]} 0.0 {Z2[k,i]}\n")
    f.write("POINT_DATA {}\n".format((N1-1) * N3))
    f.write("SCALARS data float 1\n")
    f.write("LOOKUP_TABLE default\n")
    for k in range(N3):
        for i in range(N1-1):
            f.write(f"{wp[k, i]}\n")

with open("WOA_1D_Analytical_u.vtk", "w") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("2D data\n")
    f.write("ASCII\n")
    f.write("DATASET STRUCTURED_GRID\n")
    f.write(f"DIMENSIONS {N1} 1 {N3-1}\n")
    f.write("POINTS {} float\n".format(N1 * (N3-1)))
    for k in range(N3-1):
        for i in range(N1):
            f.write(f"{X3[k,i]} 0.0 {Z3[k,i]}\n")
    f.write("POINT_DATA {}\n".format(N1 * (N3-1)))
    f.write("SCALARS data float 1\n")
    f.write("LOOKUP_TABLE default\n")
    for k in range(N3-1):
        for i in range(N1):
            f.write(f"{up[k, i]}\n")

# Plots
#==================================================

plt.figure()
plt.pcolormesh(xp, z, wp, cmap='RdBu_r', shading='gouraud')
plt.colorbar(label=r"$w$")
plt.show()

fig, ax = plt.subplots()
CS = ax.contour(X2, Z2, wp, levels=np.arange(start=-0.005, stop=0.0051, step=0.0005), colors='black')
ax.clabel(CS, fontsize=10, inline=True, fmt='%1.4f')
ax.set_xlim([-15*aval, 30*aval])
ax.set_ylim([zmin, zmax])
ax.scatter(XGR, YGR, s=1.0, color='red')
plt.show()

plt.figure()
plt.pcolormesh(x, zp, up, cmap='RdBu_r', shading='gouraud')
plt.colorbar(label=r"$u$")
plt.show()

fig, ax = plt.subplots()
CS = ax.contour(X3, Z3, up, levels=np.arange(start=-0.025, stop=0.0251, step=0.0025), colors='black')
ax.clabel(CS, fontsize=10, inline=True, fmt='%1.4f')
ax.set_xlim([-15*aval, 30*aval])
ax.set_ylim([zmin, zmax])
plt.show()
