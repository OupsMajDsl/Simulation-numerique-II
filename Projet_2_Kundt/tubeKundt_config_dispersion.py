import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

# Constantes initialisation
L = 150                         # Longueur du tube de Kundt en m
r = 1                       # Diamètre du tube en m
V_0 = 10                        # Vitesse d'oscillation du piston en x = 0
f = 1000                         # Fréquence du signal en Hz
eta = 0.8						# tube ouvert pour 0
rho = 1.2                       # Densité du milieu en kg.m^-3
c = 340                         # Célérité de l'onde 
omega = 2 * np.pi * f           # Pulsation
k = omega/c                     # Nombre d'onde
z_c = rho* c					# Impédance acoustique dépendant du milieu
R_p = 0.7						    # Coefficient de réflexion
A = 2							# Amplitude de l'onde incidente

# Dispersion et atténuation
alpha = 3e-5 * np.sqrt(f)/ r
k_d = k + (1 - 1j) * alpha

# Variables temps, espace
x = np.arange(0, L, 1/f)

# Pression, vitesse
p_i = A * np.exp(-1j * k * x)
p_r = A * R_p * np.exp(1j * k * x) 
	# somme de la pression incidente et réfléchie pour obtenir l'onde stationnaire
p_tot = np.asarray((p_i + p_r))

# attén, dispers
p_i_d = A * np.exp(-1j * k_d * x)
p_r_d = A * R_p * np.exp(1j * k_d * x) 
p_tot_d = np.asarray((p_i_d + p_r_d))

# initialisation de la figure
fig, ax = plt.subplots(1, 1)

# fonction pour ajouter la partie temporelle 
# au nombre complexe calculé et calcul en réel
# pour obtenir le signal physique prêt à tracer
def reel(cplx, time):
    return np.real(cplx * np.exp(1j * omega * time))

p_tot_re = reel(p_tot, 0.0042)
p_tot_d_re = reel(p_tot_d, 0.0042)


ax.plot(x, p_tot_re, '-', label="Champ de pression sans pertes")
ax.plot(x, p_tot_d_re, '-', label="Champ de pression avec pertes")

ax.set_ylabel("Amplitude [Pa]")
ax.set_xlabel("Longueur du tube [m]")
ax.set_title(r"[$f$ = {:.1f} Hz] - [$L$ = {:.2f} m] - [$r$ = {} m] - [$\eta$ = {:.1f}] - [$R_p$ = {:.1f}]".format(f, L, r, eta, R_p))

ax.set_xlim(0, L)
#ax.set_xticks([0, L/4, L/2, (3*L)/4, L])
ax.grid()
ax.legend()

plt.show()