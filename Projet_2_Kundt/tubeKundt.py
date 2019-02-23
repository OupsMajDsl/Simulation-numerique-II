import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

# Constantes initialisation
L = 10                          # Longueur du tube de Kundt en m
r = 0.006                           # Diamètre du tube en m
V_0 = 10                        # Vitesse d'oscillation du piston en x = 0
f = 520                         # Fréquence du signal en Hz
eta = 0.0						# tube ouvert pour 0
rho = 1.2                       # Densité du milieu en kg.m^-3
c = 340                         # Célérité de l'onde 
omega = 2 * np.pi * f           # Pulsation
k = omega/c                     # Nombre d'onde
z_c = rho* c					# Impédance acoustique dépendant du milieu
R_p = 0						# Coefficient de réflexion
A = 250							# Amplitude de l'onde incidente

# Dispersion et atténuation
alpha = 3e-5 * np.sqrt(f / r)
k_d = k + (1 - 1j) * alpha

# Variables temps, espace
x = np.arange(0, L, 0.01)
t = np.arange(0, 1, 0.00001)

# Pression, vitesse
p_i = A * np.exp(-1j * k * x)
p_r = A * R_p * np.exp(1j * k * x) 
	# somme de la pression incidente et réfléchie pour obtenir l'onde stationnaire
p_tot = np.asarray((p_i + p_r))

v_i = (A/z_c) * np.exp(-1j * k * x)
v_r = - (A/z_c) * R_p * np.exp(1j * k * x) 
	# mêmes calculs pour la vitesse mais l'amplitude est A/z_c
v_tot = np.asarray(v_i + v_r)


# attén, dispers
p_i_d = A * np.exp(-1j * k_d * x)
p_r_d = A * R_p * np.exp(1j * k_d * x) 
p_tot_d = np.asarray((p_i_d + p_r_d))

v_i_d = (A/z_c) * np.exp(-1j * k_d * x)
v_r_d = - (A/z_c) * R_p * np.exp(1j * k_d * x) 
v_tot_d = np.asarray(v_i_d + v_r_d)


if __name__ == "__main__":
	# initialisation de la figure
	fig, ax   = plt.subplots(2, 1)
	lines     = []
	# Styles de tracés identique pour les 2 subplots
	plotStyle = ['b--', 'r--', 'k', 'g']
	labels    = ["Onde incidente", "Onde réfléchie", "Somme des 2", "Dispersion"]
	for i in range(2):
		for j in range(4):
			line, = ax[i].plot([], [], plotStyle[j], label = labels[j])
			lines.append(line)

	# fonction pour ajouter la partie temporelle 
	# au nombre complexe calculé et calcul en réel
	# pour obtenir le signal physique prêt à tracer
	def reel(cplx, time):
		return np.real(cplx * np.exp(1j * omega * time))

	def animate(t_var):
		datas = [
				reel(p_i, t_var), 
				reel(p_r, t_var), 
				reel(p_tot, t_var), 
				reel(p_tot_d, t_var), 
				reel(v_i, t_var), 
				reel(v_r, t_var), 
				reel(v_tot, t_var),
				reel(v_tot_d, t_var),
				]

		# datas regroupe toutes les grandeurs calculées en partie réel
		for i in range(len(datas)):
			lines[i].set_data(x, datas[i])
		return lines

	for i in range(2):
		ax[i].set_xlim(0, L)
		ax[i].set_xticks([0, L/4, L/2, (3*L)/4, L])
		ax[i].grid()
		ax[i].legend()

# Ticks et labels pour changer la graduation du plot avec le changement de l'amplitude
	ax[0].set_yticks([-2* A, -A, 0, A, 2* A])
	ax[0].set_yticklabels(["", str(-1 * A), "0", str(A), ""])
	ax[1].set_yticks([-1.5* int((A/z_c) + 1), -1* int((A/z_c) + 1), 0, int((A/z_c) + 1), 1.5* int((A/z_c) + 1)])
	ax[1].set_yticklabels(["", "{:.2f}".format(-1 *(A/z_c)), "0", "{:.2f}".format(-1 *(A/z_c)), ""])

	ax[0].set_xticklabels([])
	ax[1].set_xticklabels([r"$0$", r"$L/4$", r"$L/2$", r"$3L/4$", r"$L$"])
	ax[0].set_title(r"[$f$ = {:.1f} Hz] - [$L$ = {:.2f} m] - [$r$ = {} m] - [$\eta$ = {:.1f}] - [$R_p$ = {:.1f}]".format(f, L, r, eta, R_p))

	ani = animation.FuncAnimation(fig, animate, frames = t, interval = 10, blit = True)
	plt.show()