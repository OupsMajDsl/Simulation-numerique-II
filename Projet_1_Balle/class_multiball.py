import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import matplotlib.colors as pltc
import random

class Balle():
    def __init__(self, nb_balle = 25, duration = 20, log = True, save = False):
        """
        Initialize the Balle class and declare the inputs parameters as well as the useful variables
        """
        self.t = np.arange(0, duration, 0.01)
        self.fig, self.ax = plt.subplots(figsize = (15, 7))
        self.nb_balle = nb_balle
        self.trace = True
        self.save = save
        self.log = log
        self.lines = []
        self.balles_x = []
        self.balles_y = []

#===========================
    def setup(self):
        """
        This setup function calculates the trajectories of each ball
        """
        g = 9.8
        r = 0.8
        def find_nearest(array, value):
            array = np.asarray(array)
            indice = (np.abs(array - value)).argmin()
            return indice
        def rand_nb(mini, maxi):
            return round(random.uniform(mini, maxi), 3)
                                            #début du calcul de la trajectoire des balles, calcul pour n rebonds
        for balle in range(self.nb_balle):
            #définition des conditions initiales
            a_0 = np.radians(rand_nb(20, 80))    #angle initial   
            v_i = rand_nb(30, 60)                 #vitesse initiale
            t_0 = rand_nb(0, int(max(self.t)-2))                 #décalage temporel
            v_0 = v_i                                     #initialisation de la vitesse de la balle
            nb_rebond = 15                                 #nombre de rebonds de chaque balle

            d_y = 0     #position initiale
            d_x = 0     
            d_0_x = 0   #offset de la position
            d_0_y = 0
            pos_x = []  #vecteurs prenant les coordonnées au cours du temps pour une seule balle
            pos_y = []

            line, = self.ax.plot([], [], 'o', markersize = 14)       #création des plots vides qui prendront les balles ensuite
            self.lines.append(line)                 #lines est la liste de plots, vide pour le moment

            for n in range(nb_rebond):                  #calcul de la trajectoire d'une balle pour n rebonds
                t_max = (2*v_0*np.sin(a_0))/g + t_0     
                t_balle = np.arange(t_0, t_max, 0.1)   #détermination du vecteur temps propre à chaque objet

                for t_var in t_balle:
                    t_var -= t_0
                    d_x = v_0 * t_var* np.cos(a_0) + d_0_x                                  #calcul de la position en x
                    d_y = (-1* (1/2)* g * t_var**2) + (v_0 * t_var * np.sin(a_0)) + d_0_y   #et en y
                    pos_x.append(d_x)
                    pos_y.append(d_y)
                v_0 = r*v_0         #après chaque rebond, la vitesse diminue selon le coefficient d'absorption r
                d_0_x = d_x         #on stocke la position x à laquelle la balle touche le sol
                d_0_y = 0           #la hauteur de la balle est réinitialisée, normalement, déjà 0
            if self.log:
                print('balle --> {}/{}'.format(balle+1, self.nb_balle))

            # Adapter à l'horloge globale t, pour permettre un décalage temporel
            # détermine le début du vecteur temps d'une balle par rapport au temps global
            t_bgn = find_nearest(self.t, t_0)       
            #avant le début du mouvement de la balle, on ajoute des 0 à son vecteur position
            for _ in range(len(self.t[0:t_bgn])):
                pos_x.insert(0, 0)      
                pos_y.insert(0, 0)
# après la fin de la trajectoire de la balle, on fait en sorte qu'elle reste, sur sa position finale, au sol
            while len(pos_x) < len(self.t):      
                pos_x.append(max(pos_x))
                pos_y.append(0)
# S'il y a des valeurs en trop par rapport au vecteur temps global, on les supprime
            while len(pos_x) > len(self.t):
                del pos_x[-1]
                del pos_y[-1]
            self.balles_x.append(pos_x)             #on stocke les coordonnées x et y de toutes les balles
            self.balles_y.append(pos_y)

#===================
    def draw(self):                                 #fonction de tracé de la classe Balle
        """
        Plots the calculated data
        """
        def init():                                 #initialize the animation
            for nb in range(self.nb_balle):
                self.lines[nb].set_data([], [])
            return self.lines            

        def animate(i):
            for nb in range(self.nb_balle):
                x = self.balles_x[nb]
                y = self.balles_y[nb]
                self.lines[nb].set_data(x[i], y[i])

            if self.log:
                print('time = {:.2f}/{:.0f}'.format(self.t[i], max(self.t)))
            return self.lines

        if self.trace:                                  #permet d'avoir une fenêtre de la taille des trajectoires max
            for i in range(len(self.balles_x)):
                self.ax.plot(self.balles_x[i], self.balles_y[i], alpha = 0)
        self.ax.set_ylim(bottom = 0)
        self.ax.set_xlim(left = 0)
        self.ax.set_xlabel('Position en x [m]')
        self.ax.set_ylabel('Position en y [m]')
        #self.ax.set_title("Multiball Trajectories Animation")

        plt.tight_layout()
        ani = animation.FuncAnimation(self.fig, animate, frames = np.arange(0, len(self.balles_x[1]) - 1, 1), 
                                                    interval = 10, blit = True, init_func=init)
        if self.save:
            ani.save(filename="Projet_1_Balle/MULTIBALL.mp4", writer = 'ffmpeg', fps = 30, bitrate = 750)
        plt.show()


def main():
    b1 = Balle(35, duration = 10, log = True, save = False)
    b1.setup()
    b1.draw()

if __name__ == "__main__":
    main()