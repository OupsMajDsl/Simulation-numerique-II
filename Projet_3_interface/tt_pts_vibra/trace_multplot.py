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
        file[:, 1] = np.log10(file[:, 1])
        FRF.append(file[:, 1])
        fq_coh.append(coh[:, 0])
        coher.append(coh[:, 1])

fig, ax = plt.subplots(y_shape, x_shape)
for x in range(0, x_shape):
    for y in range(0, y_shape):
        ax[y, x].plot(fq[x*y], FRF[x*y])

plt.savefig("trace_multplot.pdf")
plt.show()
