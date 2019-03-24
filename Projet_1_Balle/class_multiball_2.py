import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import random
"""
Version finale du tracé des balles.
Ce programme permet de simuler la trajectoire de la chute de plusieurs balles en prenant des paramètres de vitesse initiale et d'angle de départ aléatoire.
La classe Balle permet de générer les coordonnées des balles et le tracé peut être réalisé après
"""

class Balle():
    def __init__(self, duration):
        self.g = 9.8                              # accélération de la gravité
        self.r = 0.8                              # réaction du sol, amortissement de la balle
        self.t = np.arange(0, duration, 0.01)     # vecteur temps global à toutes les balles crées

        # initialisation des vecteurs stockant la trajectoire de la balle
        self.pos_x = []
        self.pos_y = []

        def rand_nb(mini, maxi):
            # cette fonction retourne un float de 2 décimales
            # aléatoire compris entre la valeur mini et la valeur maxi
            return round(random.uniform(mini, maxi), 2)

        # définition des conditions initiales
        self.a_0 = np.radians(rand_nb(20, 80))              #angle initial   
        self.v_i = rand_nb(30, 60)                          #vitesse initiale
        self.t_0 = rand_nb(0, int(max(self.t) - 2))         #décalage temporel
        self.v_0 = self.v_i                                 #initialisation de la vitesse de la balle
        self.nb_rebond = 15                                 #nombre de rebonds de chaque balle
        
        # offset de la position
        self.d_0_x = 0   
        self.d_0_y = 0

    def get_tmax(self):     # retourne la durée de la trajectoire d'une balle
        t_max = (2 * self.v_0 * np.sin(self.a_0)) / self.g + self.t_0     
        return t_max

    def change_speed(self): # quand la balle touche le sol, elle est ralentie selon l'amortissement r
        self.v_0 = self.r * self.v_0
    
    def get_x(self, t):     # retourne la position en x de la balle a t secondes
        d_x = self.v_0 * t * np.cos(self.a_0) + self.d_0_x
        return d_x
    
    def get_y(self, t):     # retourne la position en y de la balle a t secondes
        d_y = (-1* (1/2)* self.g * t**2) + (self.v_0 * t * np.sin(self.a_0)) + self.d_0_y
        return d_y
    
    def get_parab(self):  # calcul des positions d'une seule parabole
        t_max = self.get_tmax()
        t_balle = np.arange(self.t_0, t_max, 0.1)
        for t_var in t_balle:
            t_var -= self.t_0
            d_x = self.get_x(t_var)
            d_y = self.get_y(t_var)
            self.pos_x.append(d_x)
            self.pos_y.append(d_y)
        self.d_0_x = d_x

    def get_rebonds(self):  # Calcul de la trajectoire pour n rebonds
        for _ in range(self.nb_rebond):
            self.get_parab()
            self.change_speed()
    
    def get_traject(self):
        self.get_rebonds()
        t_bgn = np.abs(np.asarray(self.t) - self.t_0).argmin()
        for _ in range(len(self.t[0:t_bgn])):
            self.pos_x.insert(0, 0)      
            self.pos_y.insert(0, 0)
        while len(self.pos_x) < len(self.t):      
            self.pos_x.append(max(self.pos_x))
            self.pos_y.append(0)
        return [self.pos_x, self.pos_y]


#============================
if __name__ == "__main__":
    tot_ball = 200
    duree = 10
    balle_x = []
    balle_y = []
    lines = []
    fig, ax = plt.subplots(figsize=(15, 7))

    for n_balle in range(tot_ball):
        b = Balle(duree)
        b_traject = b.get_traject()
        balle_x.append(b_traject[0])
        balle_y.append(b_traject[1])

        line, = ax.plot([], [], 'o', markersize = 14)
        lines.append(line)
        ax.plot(balle_x[n_balle], balle_y[n_balle], 'k', alpha = 0)
        print("balle = {} / {}".format(n_balle, tot_ball))

    def init():                        
        for nb in range(tot_ball):
            lines[nb].set_data([], [])
        return lines            

    def animate(i):
        for nb in range(tot_ball):
            x = balle_x[nb]
            y = balle_y[nb]
            lines[nb].set_data(x[i], y[i])
        print("time = {:.2f} / {:.0f}".format(i / 100, (len(balle_x[1]) - 1) / 100))
        return lines

    ax.set_ylim(bottom = 0)
    ax.set_xlim(left = 0)
    ax.set_xlabel('Position en x [m]')
    ax.set_ylabel('Position en y [m]')

    plt.tight_layout()
    ani = animation.FuncAnimation(fig, animate, frames = np.arange(0, len(balle_x[1]) - 1, 1), 
                                                interval = 10, blit = True, init_func=init)
    save = False
    if save:
        ani.save(filename="Projet_1_Balle/MULTIBALL.mp4", writer = 'ffmpeg', fps = 30, bitrate = 750)
    plt.show()