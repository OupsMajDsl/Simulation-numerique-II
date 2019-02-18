import numpy as np
import matplotlib.pyplot as plt 

dt = 0.1
t = dt * np.arange(256)
sp = np.fft.fft(np.sin(2 * np.pi * t))

NFFT = np.size(t)
freq = np.fft.fftfreq(NFFT, d=dt)

plt.figure()
plt.plot(freq, np.abs(sp))

plt.show()