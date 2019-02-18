import numpy as np
import matplotlib.pyplot as plt 

fig, ax = plt.subplots(2, 2)
# nombre d'éléments dans chaque vecteur et rang de la matrice carrée
nb_elt = 500
c = 340                                 # célérité de l'onde
L = 2                                   # longueur du tube de Kundt
f = np.linspace(0, 10000, nb_elt)       # axe des fréquences
eta = np.linspace(0, 10, nb_elt)        # axe de eta
# initialisation de la matrice contenant les variations de rp
r_p = np.full((nb_elt, nb_elt), 0, dtype=complex)

for i in range(len(f)):
    for j in range(len(eta)):
        # calcul du nombre d'onde k
        k = (2 * np.pi * f[i]) / c
        # calcul d'une valeur de R_p
        r_p_fqe = (eta[j] - 1) / (eta[j] + 1) * np.exp(-2j * k * L)
        # On ajoute cette valeur dans la matrice
        r_p[i, j] = r_p_fqe

r_p = r_p.T # la méthode pcolor semble transposer la matrice
            # donc on la retranspose, pour avoir les axes dans l'ordre souhaité

# subplots et titre des subplots
ax[0, 0].set_title("Partie réelle")
im00 = ax[0, 0].pcolorfast(f, eta, np.real(r_p))
ax[0, 1].set_title("Partie imaginaire")
im01 = ax[0, 1].pcolorfast(f, eta, np.imag(r_p))
ax[1, 0].set_title("Module")
im10 = ax[1, 0].pcolorfast(f, eta, abs(r_p))
ax[1, 1].set_title("Phase")
im11 = ax[1, 1].pcolorfast(f, eta, np.angle(r_p))

# graduation des axes
for i in range(2):
    for j in range(2):
        ax[i, j].set_xlabel("f")
        ax[i, j].set_ylabel(r"$\eta$")

plt.tight_layout()
plt.show()