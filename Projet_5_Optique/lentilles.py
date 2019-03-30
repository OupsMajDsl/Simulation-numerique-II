import matplotlib.pyplot as plt 
import numpy as np

class Lentille():
    def __init__(self, r=15, a=6):
        self.r = r
        self.a = a
        #self.e = self.r - self.r * np.sqrt(1 - (((2 * self.a) ** 2) / (4 * (self.r **2))))
        self.e = 5
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

            if type_l == "biconcave":
                i_1 = np.arcsin(h / self.r)
                i_2 = np.arcsin(n * (h / self.r))
                x_r1 = self.r * np.cos(i_1) - self.r - self.e
                x_r2 = - self.r * np.cos(i_2) + self.r + self.e
                y_r1 = h + (x_r2 - x_r1) * np.tan(i_2 - i_1)

                i_2 = np.arcsin(n * (y_r1 / self.r))
                y_r2 = y_r1 + (lim - x_r2) * np.tan(i_2 - i_1)
                x = [-lim, x_r1, x_r2, lim]
                y = [h, h, y_r1, y_r2]

            elif type_l == "convexe":
                i_1 = np.arcsin(h / self.r)
                i_2 = np.arcsin(n * (h / self.r))
                x_r = self.r * np.cos(i_1) - self.r + self.e
                y_inf = h - (lim - x_r) * np.tan(i_2 - i_1)
                x = [-10, x_r, lim]
                y = [h, h, y_inf]

            elif type_l == "biconvexe":
                i_1 = np.arcsin(h / self.r)
                i_2 = np.arcsin(n * (h / self.r))
                x_r1 = - self.r * np.cos(i_1) + self.r - self.e
                x_r2 = self.r * np.cos(i_1) - self.r + self.e
                y_r1 = h - (x_r2 - x_r1) * np.tan(i_2 - i_1)
                i_1 = np.arcsin(n * (y_r1 / self.r))
                i_2 = np.arcsin(y_r1 / self.r)
                y_r2 = y_r1 + (lim - x_r2) * np.tan(i_2 - i_1)
                x = [-lim, x_r1, x_r2, lim]
                y = [h, h, y_r1, y_r2]


            return [x, y]

if __name__ == "__main__":
    # tests pour la classe lentille
    fig, ax = plt.subplots()
    rays = np.arange(-6, 6.1, 1)

    l = Lentille(r=10, a=6)
    lent_biconv = l.biconvexe()
    lent_biconc = l.biconcave()
    lent_conv = l.convexe()

    for i in rays:
        # r_v = l.rayon(type_l="convexe", h=i, n=1.5)
        # ax.plot(r_v[0], r_v[1], 'b-', lw=0.5, alpha=0.5)
        r_c = l.rayon(type_l="convexe", h=i, n=1.5)
        ax.plot(r_c[0], r_c[1], 'g-', lw=0.5)

    # ax.plot(lent_conv[0], lent_conv[1], 'k-', alpha=0.5)
    ax.plot(lent_conv[0], lent_conv[1], 'm-')

    ax.grid()
    ax.axis([-10, 37.5, -10, 10])
    plt.show()


    # def rayon_convexe(self, h=3, n=1.5):
    #     lim = 200
    #     if abs(h) > abs(self.a):
    #         x = [-lim, lim]
    #         y = [h, h]
    #     else:
    #         i_1 = np.arcsin(h / self.r)
    #         i_2 = np.arcsin(n * (h / self.r))
    #         x_refrac = self.r * np.cos(i_1) - self.r + self.e
    #         x = [-10, x_refrac, fin_trace]
    #         y_inf = h - (x[2] - x_refrac) * np.tan(i_2 - i_1)
    #         y = [h, h, y_inf]
    #     return [x, y]
    
    # def rayon_concave(self, h=3, n=1.5):
    #     lim = 200
    #     if abs(h) > abs(self.a):
    #         x = [-10, lim]
    #         y = [h, h]
    #         refl = [None]
    #     else:
    #         i_1 = np.arcsin(h / self.r)
    #         i_2 = np.arcsin(n * (h / self.r))
    #         x_refrac = self.r * np.cos(i_1) - self.r + self.e
    #         x = [-10, x_refrac, lim]
    #         tanangle = np.tan(i_2 - i_1)
    #         y_inf = ( (h / tanangle) - self.r * np.cos(i_1)) * tanangle
    #         x_refl = (self.r - self.r * np.cos(i_1)) - (h / tanangle)
    #         refl = [x_refrac, x_refl]
    #         y = [h, h, y_inf]
    #     return[x, y, refl]
