import matplotlib.pyplot as plt 
import numpy as np

class Lentille():
    def __init__(self, r=15, a=6):
        self.r = r
        self.a = a
        self.e = self.r - self.r * np.sqrt(1 - (((2 * self.a) ** 2) / (4 * (self.r **2))))
        self.y = np.linspace(-self.a, self.a + 0.01, 100)
        self.x = np.sqrt(self.r**2 - self.y**2) - self.r + self.e
# équation 2nd degré pour résolution

    def biconvexe(self):
        return [np.append(self.x, -self.x), np.append(self.y, -self.y)]

    def convexe(self):
        return [np.append(self.x, [0]), np.append(self.y, [-self.a])]
    
    def concave(self):
        pass

    def rayon_convexe(self, h=3, n=1.5):
        fin_trace = 200
        if h > self.a or h < -self.a:
            x = [-10, fin_trace]
            y = [h, h]
        else:
            i_1 = np.arcsin(h / self.r)
            i_2 = np.arcsin(n * (h / self.r))
            x_refrac = self.r * np.cos(i_1) - self.r + self.e
            x = [-10, x_refrac, fin_trace]
            y_inf = h - (x[2] - x_refrac) * np.tan(i_2 - i_1)
            y = [h, h, y_inf]
        return [x, y]
    
    def rayon_concave(self, h=3, n=1.5):
        lim = 200
        if abs(h) > abs(self.a):
            x = [-10, lim]
            y = [h, h]
            refl = [None]
        else:
            i_1 = np.arcsin(h / self.r)
            i_2 = np.arcsin(n * (h / self.r))
            x_refrac = self.r * np.cos(i_1) - self.r + self.e
            x = [-10, x_refrac, lim]
            tanangle = np.tan(i_2 - i_1)
            y_inf = ( (h / tanangle) - self.r * np.cos(i_1)) * tanangle
            x_refl = (self.r - self.r * np.cos(i_1)) - (h / tanangle)
            refl = [x_refrac, x_refl]
            y = [h, h, y_inf]
        return[x, y, refl]

if __name__ == "__main__":
    # tests pour la classe lentille
    fig, ax = plt.subplots()

    rays = np.arange(-6, 6, 0.1)
    l = Lentille(r=10, a=6)
    l_v = l.concave()

    for i in rays:
        r_v = l.rayon_concave(h=i, n=1.5)
        ax.plot(r_v[0], r_v[1], 'b-', lw=0.5)
    ax.plot(l_v[0], l_v[1], 'k-')

    ax.grid()
    ax.axis([-10, 37.5, -10, 10])
    plt.show()