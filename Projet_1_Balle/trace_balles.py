import class_multiball_2 as ball
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Utilise la classe Balle du script 'class_multiball_2.py' pour tracer la trajectoire des balles
"""

tot_ball = 50
duree = 20
x_pos = []
y_pos = []
lines = []
fig, ax = plt.subplots(figsize=(15, 7))

for n_balle in range(tot_ball):
    b = ball.Balle(duree)
    # On crée l'instance de classe b
    b_traject = b.get_traject()

    """
    b_traject contient alors les données complètes des trajectoires de la balle
    C'est une liste qui contient 2 listes sous la forme:
    b_traject = [[coordonnées x], [coordonnées y]]
    """
    x_pos.append(b_traject[0])
    y_pos.append(b_traject[1])

    # Initialisation d'une ligne par balle
    line, = ax.plot([], [], 'o', markersize = 14)
    # On ajoute chaque ligne à une liste 
    lines.append(line)
    # On trace la trajectoire globale de chaque balle pour avoir une échelle adaptée 
    # sur le graph: comme l'opacité est de 0, on ne voit pas ces tracés
    ax.plot(x_pos[n_balle], y_pos[n_balle], 'k', alpha = 0)
    # print("balle = {} / {}".format(n_balle, tot_ball))

def init():       
    # Initialisation de l'animation                 
    for nb in range(tot_ball):
        lines[nb].set_data([], [])
    return lines            

# fonction d'animation
def animate(i):
    # Pour chaque balle, on trace ses coordonnées à l'instant i
    for nb in range(tot_ball):
        x = x_pos[nb]
        y = y_pos[nb]
        lines[nb].set_data(x[i], y[i])
    print("time = {:.2f} / {:.0f}".format(i / 100, (len(x_pos[1]) - 1) / 100))
    # Affichage du temps
    return lines

ax.set_ylim(bottom = 0)
ax.set_xlim(left = 0)
ax.set_xlabel('Position en x [m]')
ax.set_ylabel('Position en y [m]')

plt.tight_layout()
ani = animation.FuncAnimation(fig, animate, frames = np.arange(0, len(x_pos[1]) - 1, 1), 
                                            interval = 10, blit = True, init_func=init)
plt.show()