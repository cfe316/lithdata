import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from lithdata.vaporpressure import *
from lithdata.utility import error_bands

# Simple plot of all the literature vapor pressures.
# Because of the extreme ranges involved it's difficult to see the differences.

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1,1,1)

colors = []
for i in range(6):
    color=next(ax._get_lines.prop_cycler)['color']
    colors.append(color)

tsteps = 200
t1 = np.linspace(1057, 2156, tsteps)
f1 = press_Browning_and_Potter
p1 = f1(t1)

t2 = np.linspace(298.14, 1599.99, tsteps)
f2 = press_NIST_webbook
p2 = f2(t2)

t3 = np.linspace(800, 1800, tsteps)
f3 = press_Davison_1968
p3 = f3(t3)
p3_minus, p3_plus = error_bands(p3, 3.6)

t4 = np.linspace(735, 915, tsteps)
f4 = press_Maucherat_1939
p4 = f4(t4)

t5 = np.linspace(1216, 1415, tsteps)
f5 = press_Vargaftik_and_Kapitonov
p5 = f5(t5)

t6 = np.linspace(453, 1573, tsteps)
f6 = press_Golubchikov
p6 = f6(t6)

fs = [f1, f2, f3, f4, f5, f6]
ts = [t1, t2, t3, t4, t5, t6]
t_lo = [tr[0]-0.1 for tr in ts]
t_hi = [tr[-1]+0.1 for tr in ts]

def trapezoid(x):
    if x < 0.25:
        return 4 * x
    if x > 0.75:
        return 4 * (1 - x)
    else:
        return 1

def scurve(x):
    if x < 0.5:
        return 2 * x**2
    else:
        return 1 - 2 * (1 - x) ** 2

def curve_a_zoid(x, complete=0.20):
    if x < complete:
        return scurve(x / complete)
    elif x > 1 - complete:
        return scurve((1 - x)/complete)
    else:
        return 1

def average_pressure(t_k):
    count = 0
    p = 0
    for i, f in enumerate(fs):
        if t_k > t_lo[i] and t_k < t_hi[i]:
            fraction_of_the_way = (t_k - t_lo[i]) / (t_hi[i] - t_lo[i])
            factor = curve_a_zoid(fraction_of_the_way)
            count += factor
            p += factor * f(t_k)
    if count > 0:
        return p / count
    else:
        return np.nan

t_min = np.min(np.array(t_lo))
t_max = np.max(np.array(t_hi))

t_k = np.linspace(t_min + 0.01, t_max -0.01, 1000)
ps = np.array([average_pressure(t) for t in t_k])
ps = np.nan_to_num(ps)
interp = interp1d(t_k, ps, kind='cubic', bounds_error=False)

ax.plot(t1, p1 / interp(t1), label='Browning and Potter, 1985', color=colors[0])
ax.plot(t2, p2 / interp(t2), label='NIST webbook, Antoine Equation fit', color=colors[1])
ax.plot(t3, p3 / interp(t3), label='Davison, 1968', color=colors[2])
ax.fill_between(t3, p3_minus / interp(t3), p3_plus / interp(t3), alpha=0.2, color=colors[2])

ax.plot(t4, p4 / interp(t4), label='Maucherat, 1939', color=colors[3])
ax.plot(t5, p5 / interp(t5), label='Vargaftik and Kapitonov, 1985', color=colors[4])
ax.plot(t6, p6 / interp(t6), label='in Golubchikov, 1996', color=colors[5])
ax.set_xlim([700,1100])
plt.legend()
plt.show()

#ax.set_yscale('log')
#ax.legend()
#ax.set_title('Literature vapor pressures, as reported in:')
#ax.set_ylim([1e-10,3e6])
#ax.set_ylabel('Pressure / Pa')
#ax.set_xlabel('Temperature / K')
#plt.show()
#