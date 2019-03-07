import matplotlib.pyplot as plt
import numpy as np

# initialisation de la matrice que l'on souhaite tracer par la suite
mat_data = np.zeros((60, 60))
# intervalle où se trouve les résonances que l'on souhaite observer 
lim = [57, 73]

DeltaF = 500            # décalage entre répétition du laser de génération et du laser de détection
Freq_laser = 42e6       # fréquence de répétition du laser de détection
f_sampling = 25e6       # échantillonag du laser

dt = DeltaF / Freq_laser / f_sampling
dt = dt * 1e9

def find_nearest(array, value):
    array = np.asarray(array)
    return (np.abs(array - value)).argmin() 

for x in range(len(mat_data[0])):
    for y in range(len(mat_data[:, 0])):
        filename = "Image/{}_{}.txt".format(x, y)
        data = np.loadtxt(filename, skiprows=26, encoding='ISO8859-1')

        time = data[:, 0]
        amp = data[:, 1]

        if amp[0] == -1000:
            # Matplotib trace un point blanc si la valeur est NaN
            mat_data[x, y] = None

        else:
            # calcul de l'amplitude pour la fft
            spec = np.abs(np.fft.fft(amp))[0:len(time)//2-1]
            spec = 20 * np.log10(spec / max(spec))
            # calcul de l'axe des fréquences pour la fft
            freq = np.fft.fftfreq(len(time), d=dt)[0:len(time)//2-1]

            filt_min = find_nearest(freq, lim[0])
            filt_max = find_nearest(freq, lim[1])

            # recherche de la frequence de résonance
            fq_reson = freq[find_nearest(spec, max(spec[filt_min:filt_max]))]

            if fq_reson > lim[1] and fq_reson < lim[0]:
                mat_data[x, y] = 0
            else:
                mat_data[x, y] = fq_reson 
        print(filename)

# mat_data = mat_data / max(mat_data)
mat_data = mat_data.T
fig, ax = plt.subplots()
im = ax.pcolorfast(mat_data, cmap="RdBu")
fig.colorbar(im, label="Fréquence [GHz]")

ax.set_title("Brillouin oscillation frequency map")
ax.set_xticks(np.arange(0, 61, 10))
ax.set_xticklabels(np.arange(0, 31, 5))
ax.set_xlabel(r"x [$\mu m$]")

ax.set_yticks(np.arange(0, 61, 10))
ax.set_yticklabels(np.arange(0, 31, 5))
ax.set_ylabel(r"y [$\mu m$]")

plt.savefig("Brillouin_freq_map.pdf")
plt.show()

# Concernant ta question qui est très pertinente, j’ai complètement oublié que 
# le vecteur temps était « bizarre » sur ces données… Si tu dois répondre à une question tout de suite, 
# le bon vecteur à déclarer est le suivant :
#     DeltaF = 500; % Hz
#     Freq_laser = 42e6; % Hz
#     f_sampling = 25e6; % Hz

#     dt = DeltaF/Freq_laser/f_sampling; % s
#     dt = dt*1e9; % ns

#     time = dt*float(np.arrange(Nt-1)); % ns

# Pour les explications, ça vient de la méthode de mesure. Le dt = 4e-8 en secondes est le temps 
# réel d’échantillonnage, mais la mesure est faite par échantillonnage optique asynchrone : en gros, 
# au lieu de mesurer tout le signal d’un seul coup, on le mesure coup par coup. Mon laser de génération 
# excite l’échantillon toutes les 1/(Freq_laser+DeltaF) secondes, évidemment mon échantillon retourne à 
# l’équilibre entre chaque excitation et il donne toujours la même réponse (il n’évolue pas). 
# Comme ça va très très vite, faire une mesure directe de la réponse est impossible. On vient donc 
# mesurer la réponse point par point (instant par instant). A chaque excitation, on regarde la réponse 
# à un instant donné. Pour changer l’instant auquel on regarde l’amplitude (de la réponse de 
# l’échantillon), le laser de détection a une fréquence de répétition (Freq_laser) légèrement 
# inférieure à celle du laser d’excitation : la différence est ici DeltaF = 500 Hz. Ainsi, au bout 
# de 2 ms, les impulsions lasers de génération et détection se retrouvent à nouveau en phase et on 
# repart sur une nouvelle mesure. En gros, pour mesurer un signal qui dure au plus 23.809 ns, il faut 
# 2 ms. On peut alors définir un temps « physique » et un temps « dilaté ». Le temps « physique » 
# correspond au 23.809 ns durant lesquelles le signal existe vraiment et le temps « dilaté » est le 
# temps sur lequel est effectivement faite la mesure. Pour passer du temps « physique » au temps « dilaté », 
# il faut multiplier par DeltaF/Freq_laser. Si tous les points accessibles ne nous intéressent pas (pour 
# limiter la taille des fichiers par exemple) on peut choisir de sous-échantillonner et donc de ne pas 
# forcément avoir un pas temporel de 1/(Freq_laser+DeltaF) sur le temps « dilaté » mais le pas temporel 
# que l’on veut : ici 1/f_sampling.

# En formule, ça donne : 
# dt_dilate = 1/f_sampling [= au plus à 1/(Freq_laser+DeltaF)] ; dt_physique = dt_dilate*DeltaF/Freq_laser