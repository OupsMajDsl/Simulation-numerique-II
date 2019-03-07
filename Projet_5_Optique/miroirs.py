import matplotlib.pyplot as plt 
import numpy as np

class Miroir():
    def __init__(self, r=15, a=6):
        # rayon du miroir
        self.r = r
        # sommets + et - du miroir
        self.a = a
        # épaisseur du dioptre
        # self.e = e
        self.e = self.r - self.r * np.sqrt(1 - (((2 * self.a) ** 2) / (4 * (self.r **2))))
        # equations x et y de la forme du miroir sphérique
        self.y = np.linspace(-self.a, self.a + 0.01, 100)
        self.x = np.sqrt(self.r**2 - self.y**2) - self.r + self.e

    def convexe(self):
        # permet de tracer un miroir convexe
        return [-self.x, self.y]
    
    def concave(self):
        return [self.x, self.y]
 
    def rayon(self, type_m="convexe" ,h=3, n=1.5):
        # retourne l'équation de la trajectoire d'un rayon après réflexion 
        # d'un miroir de type type_m
        
        # jusqu'où tracer les rayons
        lim = 200
        # si la hauteur dépasse le sommet (+ ou -) du miroir
        if abs(h) > abs(self.a):
            # on trace alors un rayon qui va tout droit 
            x = [-lim, lim]
            y = [h, h] 

        else:
            # calcul de l'angle d'incidence
            a_i = np.arcsin(h / self.r)
            # dans un miroir, angle réfléchi identique à angle incident
            a_r = a_i

            if type_m == "concave":
                # inversion de la forme du miroir concave donne la forme d'un miroir convexe
                x_mir = self.r * np.cos(a_i) - self.r + self.e
                x = [-lim, x_mir, -lim]

                y_inf = h - (lim - x_mir) * np.tan(2 * a_r)
                y = [h, h, y_inf]
                return [x, y]

            elif type_m == "convexe":
                x_mir =  - (self.r * np.cos(a_i) - self.r + self.e)
                x = [-lim, x_mir, -lim]

                y_inf = h + (lim - x_mir) * np.tan(2 * a_r)
                y = [h, h, y_inf]
            return [x, y]



if __name__ == "__main__":
    # Test pour la classe miroir 
    fig, ax = plt.subplots(1, 1, figsize=(20, 15))
    rays = np.arange(-6, 6, 0.1)

    m = Miroir(r=15, a=6)
    miroir = m.convexe()
    ax.plot(miroir[0], miroir[1], 'k-')

    for i in rays:
        rayon = m.rayon(type_m="convexe", h=i)
        ax.plot(rayon[0], rayon[1], 'b', lw=0.5)

    ax.grid()
    ax.axis([-10, 10, -10, 10])
    plt.show()