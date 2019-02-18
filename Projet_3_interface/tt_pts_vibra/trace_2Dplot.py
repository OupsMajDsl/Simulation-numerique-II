import os
import numpy as np
import matplotlib.pyplot as plt 

x_shape = 3
y_shape = 5
fq =  []
FRF = []
fq_coh = []
coher = []
fig, ax = plt.subplots(1, 1)
pos = [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35]
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


cmap = plt.get_cmap('PiYG')
colormesh = ax.pcolormesh(FRF, cmap=cmap)
colorbar = fig.colorbar(colormesh)

ax.set_yticks(np.arange(0, 15, 1))
ax.set_yticklabels([str(pos[i]) for i in range(len(pos))])
colorbar.set_label("Amplitude")
ax.set_ylabel("Position (indice)")
ax.set_xlabel("Fréquence [Hz]")
ax.grid()


plt.tight_layout()
plt.savefig("trace_2Dplot.pdf")
plt.show()