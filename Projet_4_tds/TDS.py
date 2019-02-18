import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec

# Fonction qui importe un fichier à partir du nom et du chemin absolu
def load_ExpData(filename, path):
    # file comprend le chemin complet demandé dans le premier argument de np.loadtxt
    file = "{}/{}".format(path, filename)
    # on charge toutes les données dans data
    data = np.loadtxt(file, skiprows=3)

    time = data[:, 0]
    amp = data[:, 1]
    # pas du temps 
    dt = time[1] - time[0]
    # calcul de l'amplitude pour la fft
    spec = np.fft.fft(amp)
    # calcul de l'axe des fréquences pour la fft
    freq = np.fft.fftfreq(len(time), d=dt)
    # on retourne toutes nos valeurs calculées
    return time, amp, spec, freq

def find_nearest(array, value):
    array = np.asarray(array)     # on vérifie que array est bien un vecteur
    # retourne la plus petite différence entre la value et le vecteur
    # càd qu'on retourne l'indice de la valeur la plus proche de value
    return (np.abs(array - value)).argmin() 

filename = "time_rawsignals_84GPa_nice.txt"
path = "/home/mathieu/OneDrive/Documents/S4/Sim_numerique/Projet_4_tds"
# avec bad, pic impulsionnel beaucoup plus élevé donc variations moins visibles
# La fonction retourne un t-uple donc on unpack directement dans les variables dont on a besoin
time, amp, spec, freq = load_ExpData(filename, path)

# amplitudes en dB
spec = np.abs(np.asarray(spec))

spec = 20 * np.log10(spec / max(spec))

# recherche de tous les indices recherchés pour les intervalles demandés
i_015 = find_nearest(time, 0.15)
i_04 = find_nearest(time, 0.4)
i_045 = find_nearest(time, 0.45) 
i_07 = find_nearest(time, 0.7)
i_09 = find_nearest(time, 0.9)
i_20 = find_nearest(time, 2.0)

# pas temporel
dt = time[1] - time[0]

# calcul des fft sur les intervalles demandés
amp1 = np.abs(np.fft.fft(amp[i_015:i_04]))
amp1 = 20 * np.log10(amp1 / max(amp1))
fq1 = np.fft.fftfreq(len(time[i_015:i_04]), d=dt)
amp2 = np.abs(np.fft.fft(amp[i_045:i_07]))
amp2 = 20 * np.log10(amp2 / max(amp2))
fq2 = np.fft.fftfreq(len(time[i_045:i_07]), d=dt)
amp3 = np.abs(np.fft.fft(amp[i_09:i_20]))
amp3 = 20 * np.log10(amp3 / max(amp3))
fq3 = np.fft.fftfreq(len(time[i_09:i_20]), d=dt)


# Création d'une grille 3x3 pour tout tracer
gs = gridspec.GridSpec(3, 3)
# Toute la ligne 1
ax_tp = plt.subplot(gs[0, :])
# Toute la ligne 2
ax_fq = plt.subplot(gs[1, :])
# Les échantillons se partagent la ligne restante
ax_spl1 = plt.subplot(gs[2, 0])             # 0.15 --> 0.4
ax_spl2 = plt.subplot(gs[2, 1])             # 0.45 --> 0.7    
ax_spl3 = plt.subplot(gs[2, 2])             # 0.9 --> 2     ns

ax_tp.plot(time, amp)
ax_tp.set_xlabel("Temps [ns]")
ax_tp.set_ylabel("Amplitude")

# Pour tracer seulement les fréquences positives
ax_fq.plot(freq[0:len(time)//2-1], spec[0:len(time)//2-1])
ax_fq.set_xlabel("Fréquence [GHz]")
ax_fq.set_ylabel("Amplitude")

ax_spl1.plot(fq1[0:len(time[i_015:i_04])//2-1], amp1[0:len(time[i_015:i_04])//2-1])
ax_spl1.set_title("[0.15; 4]")
ax_spl2.plot(fq2[0:len(time[i_045:i_07])//2-1], amp2[0:len(time[i_045:i_07])//2-1])
ax_spl2.set_title("[0.45; 0.7]")
ax_spl3.plot(fq3[0:len(time[i_09:i_20])//2-1], amp3[0:len(time[i_09:i_20])//2-1])
ax_spl3.set_title("[0.9; 2]")

plt.tight_layout()
plt.show()