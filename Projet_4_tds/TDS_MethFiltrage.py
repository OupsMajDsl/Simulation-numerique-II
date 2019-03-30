import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import scipy.signal as sig
from scipy.optimize import curve_fit
import TDS


# chemin du fichier à traiter
path = "/home/mathieu/OneDrive/Documents/S4/Sim_numerique/Projet_4_tds"
# nom du fichier à traiter
filename = "time_rawsignals_84GPa_nice.txt"
# avec bad, pic impulsionnel beaucoup plus élevé donc variations moins visibles
# La fonction retourne un t-uple donc on unpack directement dans les variables dont on a besoin

time, amp, spec, freq = TDS.load_ExpData(filename, path)

# amplitudes en dB
spec = np.abs(np.asarray(spec))
spec = 20 * np.log10(spec / max(spec))

# pas temporel du signal
dt = time[1] - time[0]
fs = 1/dt
nyq = 0.5 * fs

#====== Création de la figure et des axes
fig, ax = plt.subplots(6, 2, figsize=(15, 21.22), tight_layout=True)
meths = ["diff", "filt", "moy_gliss", "pol_fit", "exp_fit"]
colors = ["m", "g", "b", "k", "r"]

for i in range(len(meths)):
    filt_temp = TDS.pre_treatment(time, amp, meth=meths[i], lst_param=[40, 150])
    filt_spec = np.fft.fft(filt_temp)
    filt_spec = np.abs(np.asarray(filt_spec[0:len(time)//2-1]))
    filt_spec = 20 * np.log10(filt_spec / max(filt_spec))
    freq = freq[0:len(time)//2-1]
    spec = spec[0:len(time)//2-1]
    ax[i+1, 0].set_title("Tracé temporel filtré, méthode {}".format(meths[i]))
    ax[i+1, 0].plot(time, filt_temp, '{}'.format(colors[i]))
    ax[i+1, 1].set_title("Spectre filtré, méthode {}".format(meths[i]))
    ax[i+1, 1].plot(freq, filt_spec, '{}'.format(colors[i]))

ax[0, 0].set_title("Signal temporel brut")
ax[0, 0].plot(time, amp)
ax[0, 1].set_title("Spectre brut")
ax[0, 1].plot(freq, spec)

for i in range(len(ax[:, 0])):
    ax[i, 0].set_xlabel("Temps [ns]")
    ax[i, 1].set_xlabel("Fréquence [GHz]")
    for j in range(2):
        ax[i, j].set_ylabel("Amplitude")
        ax[i, j].grid()

plt.tight_layout()
plt.savefig("tds_methfilt.pdf")
plt.show()