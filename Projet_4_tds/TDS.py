import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import scipy.signal as sig
from scipy.optimize import curve_fit

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

def pre_treatment(time, amp, meth="pol_fit", lst_param=[0, 20]):
    meths = ["diff", "filt", "moy_gliss", "pol_fit", "exp_fit"]
    dt = time[1] - time[0]
    fs = 1/dt
    nyq = 0.5 * fs

    # méthode de la dérivée 
    if meth == meths[0]:
        # variation de temps 
        df = np.zeros(time.shape)
        for t in range(len(time)):
            if t != 0 and t != len(time)-1: 
                # formule discrétisée de la dérivée 
                df[t] = (amp[t + 1] - amp[t - 1]) / (2 * dt)
            # prendre en compte le début de la liste et la fin
            elif t == 0: 
                df[0] = (amp[1] - amp[0]) / (1 * dt)
            elif t == len(time) - 1:
                df[-1] = (amp[-1] - amp[-2]) / (1 * dt)
        return df
    
    # if meth == meths[0]:
    #     return np.diff(amp)

    # Filtrage avec scipy
    if meth == meths[1]:    
        lowcut = lst_param[0] / nyq
        highcut = lst_param[1] / nyq
        num, denom = sig.butter(3, [lowcut, highcut], btype="bandpass")
        filtre = sig.filtfilt(num, denom, amp)
        return filtre

    # calcul de moyenne et filtrage
    if meth == meths[2]:
        print(len(amp))        
        n = 200
        moy_amp = np.zeros_like(amp)
        for i in range(len(time)):
            dbt_fen = i - n//2
            fin_fen = i + n//2
            moy_amp[i] = np.mean(amp[dbt_fen: fin_fen]) 
        return moy_amp

    # Polyfit 
    if meth == meths[3]:
        polyfit = np.polyfit(time, amp, lst_param[1])
        fitted_curve = np.poly1d(polyfit)
        fitted_curve = fitted_curve(time)
        return fitted_curve
    
    if meth == meths[4]:
        def func(x, a, b, c, d, e):
            amp_max = find_nearest(amp, max(amp))
            t_0 = time[amp_max]
            return a * np.exp(-b * (time - t_0)) + c + d * np.exp(-e * (time - t_0))    
        popt, pcov = curve_fit(func, time, amp, maxfev=10000)
        return func(time, *popt)

if __name__ == "__main__":
    # chemin du fichier à traiter
    path = "/home/mathieu/OneDrive/Documents/S4/Sim_numerique/Projet_4_tds"
    # nom du fichier à traiter
    filename = "time_rawsignals_84GPa_nice.txt"
    # avec bad, pic impulsionnel beaucoup plus élevé donc variations moins visibles
    # La fonction retourne un t-uple donc on unpack directement dans les variables dont on a besoin

    time, amp, spec, freq = load_ExpData(filename, path)

    # amplitudes en dB
    spec = np.abs(np.asarray(spec))
    spec = 20 * np.log10(spec / max(spec))

    # recherche de tous les indices recherchés pour les intervalles demandés
    i_015 = find_nearest(time, 0.15)
    i_04  = find_nearest(time, 0.4)
    i_045 = find_nearest(time, 0.45) 
    i_07  = find_nearest(time, 0.7)
    i_09  = find_nearest(time, 0.9)
    i_20  = find_nearest(time, 2.0)

    # pas temporel du signal
    dt = time[1] - time[0]
    fs = 1/dt
    nyq = 0.5 * fs

    # calcul des fft sur les intervalles demandés
    amp1 = np.abs(np.fft.fft(amp[i_015:i_04]))
    amp1 = 20 * np.log10(amp1 / max(amp1))
    fq1  = np.fft.fftfreq(len(time[i_015:i_04]), d=dt)
    amp2 = np.abs(np.fft.fft(amp[i_045:i_07]))
    amp2 = 20 * np.log10(amp2 / max(amp2))
    fq2  = np.fft.fftfreq(len(time[i_045:i_07]), d=dt)
    amp3 = np.abs(np.fft.fft(amp[i_09:i_20]))
    amp3 = 20 * np.log10(amp3 / max(amp3))
    fq3  = np.fft.fftfreq(len(time[i_09:i_20]), d=dt)


    #====== Création de la figure et des axes
    fig = plt.figure(figsize=(20, 15), tight_layout=True)
    # Création d'une grille 3x3 pour tout tracer
    gs = gridspec.GridSpec(3, 3)
    # Toute la ligne 1
    ax_tp = fig.add_subplot(gs[0, :])
    # Toute la ligne 2
    ax_fq = fig.add_subplot(gs[1, :])
    # Les échantillons se partagent la ligne restante
    ax_spl1 = fig.add_subplot(gs[2, 0])             # 0.15 --> 0.4
    ax_spl2 = fig.add_subplot(gs[2, 1])             # 0.45 --> 0.7    
    ax_spl3 = fig.add_subplot(gs[2, 2])             # 0.9 --> 2     ns

    #======= Filtrage sur la figure principale
    meth = "diff"
    filt_temp = pre_treatment(time, amp, meth=meth, lst_param=[40, 150])
    # ax_tp.plot(time, filt_temp, 'k')
    ax_tp.plot(time, amp)
    ax_tp.set_xlabel("Temps [ns]")
    ax_tp.set_ylabel("Amplitude")
    ax_tp.set_title("Filtrage = {}".format(meth))

    filt_spec = np.fft.fft(filt_temp)
    filt_spec = np.abs(np.asarray(filt_spec[0:len(time)//2-1]))
    filt_spec = 20 * np.log10(filt_spec / max(filt_spec))

    freq = freq[0:len(time)//2-1]
    spec = spec[0:len(time)//2-1]

    # Pour tracer seulement les fréquences positives
    ax_fq.plot(freq, spec)
    # ax_fq.plot(freq, filt_spec)
    ax_fq.set_xlabel("Fréquence [GHz]")
    ax_fq.set_ylabel("Amplitude")


    ax_spl1.plot(fq1[0:len(time[i_015:i_04])//2-1], amp1[0:len(time[i_015:i_04])//2-1])
    ax_spl1.set_title("[0.15; 4]")
    ax_spl2.plot(fq2[0:len(time[i_045:i_07])//2-1], amp2[0:len(time[i_045:i_07])//2-1])
    ax_spl2.set_title("[0.45; 0.7]")
    ax_spl3.plot(fq3[0:len(time[i_09:i_20])//2-1], amp3[0:len(time[i_09:i_20])//2-1])
    ax_spl3.set_title("[0.9; 2]")

    print(len(time))
    plt.show()