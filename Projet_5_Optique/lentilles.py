import matplotlib.pyplot as plt 
import numpy as np

class Lentille():
    def __init__(self, r=15, a=6):
        self.r = r
        self.a = a
        self.e = self.r - self.r * np.sqrt(1 - (((2 * self.a) ** 2) / (4 * (self.r **2))))
        # self.e = 10
        self.y = np.linspace(-self.a, self.a + 0.01, 100)
        self.x = np.sqrt(self.r**2 - self.y**2) - self.r + self.e
# équation 2nd degré pour résolution

    def biconvexe(self):
        return [np.append(self.x, -self.x), np.append(self.y, -self.y)]

    def convexe(self):
        return [np.append(self.x, self.x[0]), np.append(self.y, [-self.a])]
    
    def biconcave(self):
        part1_x = np.append(-self.x + 2 * self.e, self.x[0] - 2 * self.e)
        part2_x = np.append(self.x - 2 * self.e, self.x[-1] + 2 * self.e)
        part1_y = np.append(self.y, self.y[-1])
        part2_y = np.append(-self.y, self.y[0])
        return [np.append(part1_x, part2_x), np.append(part1_y, part2_y)]

    def rayon(self, type_l="biconvexe" ,h=3, n=1.5):
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
            # Position du rayon au niveau du miroir
            x_mir = self.r * np.cos(a_i) - self.r + self.e
            # Position du rayon en y à l'infini
            y_inf = (lim - x_mir) * np.tan(2 * a_r)


# calculs de tous les éléments nécessaire  pour établir les trajectoires des rayons
            if type_l == "biconcave":
                i_1 = np.arcsin(h / self.r)
                i_2 = np.arcsin(n * (h / self.r))
                x_r1 = self.r * np.cos(i_1) - self.r - self.e
                x_r2 = - self.r * np.cos(i_2) + self.r + self.e
                y_r1 = h + (x_r2 - x_r1) * np.tan(i_2 - i_1)
                # si le rayon est au-dessus/ en-dessous du dioptre, il part tout droit
                if abs(y_r1) > abs(self.a):
                    x_r2 = lim
                    y_r1 = h + (x_r2 - x_r1) * np.tan(i_2 - i_1)
                i_2 = np.arcsin(n * (y_r1 / self.r))
                y_r2 = y_r1 + (lim - x_r2) * np.tan(i_2 - i_1)
                x = [-lim, x_r1, x_r2, lim]
                y = [h, h, y_r1, y_r2]
                x_virt = [x_r2, -lim]
                y_r2_virt = y_r1 - (lim - x_r2) * np.tan(i_2 - i_1)
                y_virt = [y_r1, y_r2_virt]

            elif type_l == "convexe":
                i_1 = np.arcsin(h / self.r)
                i_2 = np.arcsin(n * (h / self.r))
                x_r = self.r * np.cos(i_1) - self.r + self.e
                y_inf = h - (lim - x_r) * np.tan(i_2 - i_1)
                x = [-10, x_r, lim]
                y = [h, h, y_inf]
                x_virt = []
                y_virt = []

            elif type_l == "biconvexe":
                i_1 = np.arcsin((1/n) * (h / self.r))
                i_2 = np.arcsin(n * (h / self.r))
                x_r1 = - self.r * np.cos(n * i_1) + self.r - self.e
                x_r2 = - x_r1
                y_r1 = h - (x_r2 - x_r1) * np.tan(i_2 - i_1)
                i_1 = np.arcsin(n * (y_r1 / self.r))
                i_2 = np.arcsin(y_r1 / self.r)
                y_r2 = y_r1 + (lim - x_r2) * np.tan(i_2 - n * i_1)
                x = [-lim, x_r1, x_r2, lim]
                y = [h, h, y_r1, y_r2]
                x_virt = []
                y_virt = []
            return [x, y, x_virt, y_virt]

if __name__ == "__main__":
    # tests pour la classe lentille
    fig, ax = plt.subplots(1, 1, figsize=(20, 15))
    # liste contenant les hauteurs des rayons que l'on veut tracer
    rays = np.arange(-1, 1, 0.1)

    # on crée un objet de chaque type
    l = Lentille(r=10, a=6)
    lent_biconv = l.biconvexe()
    lent_biconc = l.biconcave()
    lent_conv = l.convexe()

    # La boucle sert à calculer et à tracer chaque rayon
    # réel ou virtuel
    for i in rays:
        r_c = l.rayon(type_l="biconcave", h=i, n=1.5)
        # rayon réel
        ax.plot(r_c[0], r_c[1], 'b', lw=0.5, alpha=.8)
        # rayon virtuel
        ax.plot(r_c[2], r_c[3], 'r--', lw=0.5)

    # finalement, on trace le dioptre
    ax.plot(lent_biconc[0], lent_biconc[1], 'k')

    ax.grid()
    ax.axis([-15, 15, -10, 10])
    plt.show()