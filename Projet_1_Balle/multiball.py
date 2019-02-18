import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import matplotlib.colors as pltc
import random

# class Balle():
#     def __init__(self, a_0 = 45, v_i = 30, d_x = 0, t_0 = 0.2, nb_rebond = 5, r = 0.5, g = 9.8):
#         self.a_0 = a_0
g = 9.8
r = 0.9
trace = True
nb_rebond = 10
nb_balle = 75

fig, ax = plt.subplots(figsize = (12, 5))
lines = []
balles_x = []
balles_y = []

def find_nearest(array, value):
    array = np.asarray(array)
    indice = (np.abs(array - value)).argmin()
    return indice

#définition des conditions initiales
t = np.arange(0, 20, 0.01)

for i in range(nb_balle):
    a_0 = random.randrange(20, 80)
    v_i = random.randrange(30, 60)
    t_0 = random.randrange(1, 10)
    d_y = 0
    d_x = 0
    pos_x = []
    pos_y = []
    v_0 = v_i
    d_0_x = 0
    d_0_y = 0
    a_0 = np.radians(a_0)

    line, = ax.plot([], [], 'o', markersize = 14)
    lines.append(line)

    #début d'une balle, calcul complet pour n rebonds
    for n in range(nb_rebond):
        t_max = (2*v_0*np.sin(a_0))/g + t_0
        t_balle = np.arange(t_0, t_max, 0.1)

        for t_var in t_balle:
            t_var -= t_0
            d_x = v_0 * t_var* np.cos(a_0) + d_0_x
            d_y = (-1* (1/2)* g * t_var**2) + (v_0 * t_var * np.sin(a_0)) + d_0_y 
            pos_x.append(d_x)
            pos_y.append(d_y)
        v_0 = r*v_0
        d_0_x = d_x
        d_0_y = 0
    print('balle', i+1)

#Adapter à l'horloge globale t
    t_bgn = find_nearest(t, t_0)
    t_end = find_nearest(t, t_max)
    for i in range(len(t[0:t_bgn])):
        pos_x.insert(0, 0)
        pos_y.insert(0, 0)
    while len(pos_x) < len(t):
        pos_x.append(max(pos_x))
        pos_y.append(0)
    while len(pos_x) > len(t):
        del pos_x[-1]
        del pos_y[-1]

    balles_x.append(pos_x)
    balles_y.append(pos_y)

def animate(i):
    for nb in range(nb_balle):
        x = balles_x[nb]
        y = balles_y[nb]
        lines[nb].set_data(x[i], y[i])
    print('time = {:.2f}/{:.0f}'.format(t[i], max(t)))
    return lines

ax.set_xlabel('Position en x [m]')
ax.set_ylabel('Position en y [m]')
#ax.axis([0, 25, 0, 150])
if trace:
    for i in range(len(balles_x)):
        ax.plot(balles_x[i], balles_y[i], 'k--', alpha = 0)
plt.tight_layout()
ani = animation.FuncAnimation(fig, animate, frames = np.arange(0, len(balles_x[1]) - 1, 1), interval = 10, blit = True)
#ani.save(filename="MULTIBALL.mp4", writer = 'ffmpeg', fps = 15, bitrate = 1000)
plt.show()