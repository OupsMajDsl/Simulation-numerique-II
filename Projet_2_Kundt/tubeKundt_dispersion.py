import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

# Constantes initialisation
L = 10                          # Longueur du tube de Kundt en m
r = 0.0068                       # Diamètre du tube en m
V_0 = 10                        # Vitesse d'oscillation du piston en x = 0
f = 500                         # Fréquence du signal en Hz
eta = 0.0						# tube ouvert pour 0
rho = 1.2                       # Densité du milieu en kg.m^-3
c = 340                         # Célérité de l'onde 
omega = 2 * np.pi * f           # Pulsation
k = omega/c                     # Nombre d'onde
z_c = rho* c					# Impédance acoustique dépendant du milieu
R_p = 1						    # Coefficient de réflexion
A = 2							# Amplitude de l'onde incidente

# Dispersion et atténuation
alpha = 3e-5 * np.sqrt(f) / r
k_d = k + (1 - 1j) * alpha

# Variables temps, espace
x = np.linspace(0, L, 10000)

# Pression, vitesse
p_i = A * np.exp(-1j * k * x)
p_r = A * R_p * np.exp(1j * k * x) 
	# somme de la pression incidente et réfléchie pour obtenir l'onde stationnaire
p_tot = np.asarray((p_i + p_r))

# attén, dispers
p_i_d = A * np.exp(-1j * k_d * x)
p_r_d = A * R_p * np.exp(1j * k_d * x) 
p_tot_d = np.asarray((p_i_d + p_r_d))

v_i = (A/z_c) * np.exp(-1j * k * x)
v_r = - (A/z_c) * R_p * np.exp(1j * k * x) 
	# mêmes calculs pour la vitesse mais l'amplitude est A/z_c
v_tot = np.asarray(v_i + v_r)

# initialisation de la figure
fig, ax = plt.subplots(1, 1)

# fonction pour ajouter la partie temporelle 
# au nombre complexe calculé et calcul en réel
# pour obtenir le signal physique prêt à tracer
def reel(cplx, time):
    return np.real(cplx * np.exp(1j * omega * time))

p_tot_re = reel(p_tot, 0)
p_tot_d_re = reel(p_tot_d, 0)

p_tot_re_T = reel(p_tot, 1 / (2 *f))
p_tot_d_re_T = reel(p_tot_d, 1 / (2 *f))

ax.plot(x, p_tot_re_T, label="1/2 T, pas dispers")
ax.plot(x, p_tot_d_re_T, label="1/2 T, dispers")
ax.plot(x, p_tot_re, '--', label="t=0, pas dispers")
ax.plot(x, p_tot_d_re, '--', label="t=0, dispers")

ax.set_xlim(0, L)
ax.set_xticks([0, L/4, L/2, (3*L)/4, L])
ax.grid()
ax.legend()

plt.show()