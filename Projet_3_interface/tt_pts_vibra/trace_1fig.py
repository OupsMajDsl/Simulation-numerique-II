import numpy as np
import matplotlib.pyplot as plt 

x_shape = 3
y_shape = 5
fq =  []
FRF = []
fq_coh = []
coher = []
path = "/home/mathieu/OneDrive/Documents/S4/Projet/3e_seance/tt_pts_vibra/"

for x in range(1, x_shape + 1):
    for y in range(1, y_shape + 1):
        filename = path+"rep_freq_{}{}/FRF_ModPhase.txt".format(x, y)
        coherence = path+"rep_freq_{}{}/Coherences.txt".format(x, y)
        file = np.loadtxt(filename, skiprows=5)
        coh = np.loadtxt(coherence, skiprows=5)
        fq.append(file[:, 0])
        #file[:, 1] = np.log10(file[:, 1])
        FRF.append(file[:, 1])
        fq_coh.append(coh[:, 0])
        coher.append(coh[:, 1])

fig, ax = plt.subplots(2, 1)
for i in range(x_shape * y_shape):
    ax[0].plot(fq[i], FRF[i])
ax[0].set_title("FRF de tous les points")
ax[1].set_title("Moyenne des FRF")
ax[1].plot(fq[0], np.asarray(FRF).mean(0))

for i in range(2):
    ax[i].set_xlabel("Fréquence [Hz]")
    ax[i].set_ylabel("Amplitude [dB]")
    ax[i].grid()
    ax[i].set_xlim(10, 1000)

plt.savefig("trace_1fig.pdf")
plt.show()