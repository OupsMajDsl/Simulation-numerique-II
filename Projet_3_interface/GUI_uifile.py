import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QLabel, QCheckBox, QComboBox, 
                            QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox,
                            QSpacerItem, QFrame)
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd

from GUI_template import Ui_Dialog


class GUI(QDialog):
    def __init__(self):
        super(GUI, self).__init__()
        # chargement du fichier interface créé avec Qt Designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # titre de la fenêtre
        self.setWindowTitle("L'interface du reste de ma vie (étudiante!)")
        # icone de la fenêtre dans la barre des tâches
        self.setWindowIcon(QIcon('icon.png'))

        # création de la figure
        self.fig = Figure(figsize=(20, 10), dpi=100)
        self.fig.tight_layout()
        # axe vide
        self.ax = self.fig.add_subplot(111)
        self.data_init = np.zeros((10, 2))


        self.init_vars_1()
        self.init_vars_2()
        self.connectSignals()


# Messages d'erreurs
    def showLoadError(self):
        msg = QMessageBox.warning(self, 'Erreur', "Le dossier chargé ne contient pas ce type de données")
    def NoDataLoaded(self):
        msg = QMessageBox.warning(self, 'Erreur', "Aucune donnée n'a été chargée")

    def init_vars_1(self):
        self.folder_1 = ""
        self.loaded_1 = False
        self.data_folder_1 = [self.data_init, self.data_init]
        self.ui.folder_status_1.setText("Aucun dossier chargé")

    def init_vars_2(self):
        self.folder_2 = ""
        self.loaded_2 = False
        self.data_folder_2 = [self.data_init, self.data_init]
        self.ui.folder_status_2.setText("Aucun dossier chargé")


    def connectSignals(self):
        # Chargement des éléments de matplotlib dans les layouts
        # création des objets matplotlib compatibles avec Qt
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Ajout dans les layout prévus
        self.ui.toolbarLay.addWidget(self.toolbar)
        self.ui.canvasLay.addWidget(self.canvas)
        # Boutons de chargement de fichiers
        self.ui.folder_1.clicked.connect(self.getFolder)
        self.ui.folder_2.clicked.connect(self.getFolder)
        # Boutons pour enlever le fichier
        self.ui.remove_1.clicked.connect(self.removeFolder)
        self.ui.remove_2.clicked.connect(self.removeFolder)
        self.ui.actualiser.clicked.connect(self.loadData)

    # Fonction pour ouvrir l'arboresence de fichiers
    def openFolder(self):
        try:
            # fileName contient le chemin absolu du fichier sélectionné
            folderName = QFileDialog.getExistingDirectory(self, "Ouvrir un dossier", "")
            return folderName
        # Si on ferme la boîte de dialogue avant sélection d'un fichier, apparition d'une OSError
        except OSError:
            pass

    def getFolder(self):
        folder = self.openFolder()
        sender = self.sender()
        if sender.text() == "Dossier 1":
            self.ui.folder_status_1.setText("Dossier chargé -->"+folder)
            self.folder_1 = folder
            self.loaded_1 = True
        elif sender.text() == "Dossier 2":
            self.ui.folder_status_2.setText("Dossier chargé -->"+folder)
            self.folder_2 = folder
            self.loaded_2 = True

    def loadData(self):
        folder, data1, data2 = [[], [], []]
        noerror = True
        if self.loaded_1:
            folder.append(self.folder_1)
        if self.loaded_2:
            folder.append(self.folder_2)
        
        if folder == []:
            self.NoDataLoaded()

        else:
            for i in range(len(folder)):
                if self.ui.comboBox.currentText() == "FRF":
                    try:
                        data1 = np.loadtxt(folder[i]+"/FRF_ModPhase.txt", skiprows=1)
                        data2 = np.loadtxt(folder[i]+"/Coherences.txt", skiprows=1)
                        self.titles = ["FRF", "Cohérence"]
                        self.ylabels = ["Amplitude", "Cohérence relative"]
                        self.xlabels = ["Fréquence", "Fréquence"]
                    except OSError:
                        noerror = False

                if self.ui.comboBox.currentText() == "Spectre":
                    try:
                        data1 = np.loadtxt(folder[i]+"/PowerSpectrum.txt", skiprows=1)
                        data2 = data1
                        self.titles = ["Spectre", "Spectre"]
                        self.ylabels = ["Amplitude", "Amplitude"]
                        self.xlabels = ["Fréquence", "Fréquence"]

                    except OSError:
                        noerror = False

                if self.ui.comboBox.currentText() == "Temporel":
                    try:
                        data1 = np.loadtxt(folder[i]+"/TemporalData.txt", skiprows=1)
                        data2 = self.fft(data1)
                        self.titles = ["Temporel", "FFT"]
                        self.ylabels = ["Amplitude", "Amplitude"]
                        self.xlabels = ["Temps", "Fréquence"]
                    except OSError:
                        noerror = False
                if i == 0:
                    self.data_folder_1 = [data1, data2]
                if i == 1:
                    self.data_folder_2 = [data1, data2]

            if noerror:
                self.plot()
            else:
                self.showLoadError()

    def fft(self, data):
        amp = data[:, 1]
        time = data[:, 0]
        dt = time[1] - time[0]

        spec = np.abs(np.fft.fft(amp))
        spec = 20 * np.log10(spec / max(spec))
        spec = spec[0:len(time)//2-1]

        freq = np.fft.fftfreq(len(time), d=dt)
        freq = freq[0:len(time)//2-1]

        data_out = np.zeros((len(freq), 2))
        for x in range(len(data_out[:, 0])):
            data_out[x, 0] = freq[x]
            data_out[x, 1] = spec[x]
        return data_out


    def plot(self):
        #reinitialiser le plot précédent
        self.fig.clear()
        # create an axis
        ax1 = self.fig.add_subplot(211)
        ax2 = self.fig.add_subplot(212)
        ax = [ax1, ax2]

        for i in range(len(ax)):
            data1 = self.data_folder_1[i]
            data2 = self.data_folder_2[i]

            if self.ui.dbX.isChecked() and self.ui.logY.isChecked():
                ax[i].loglog(data1[:, 0], data1[:, 1], label="Dossier 1")
                ax[i].loglog(data2[:, 0], data2[:, 1], label="Dossier 2")
            elif self.ui.dbX.isChecked():
                ax[i].semilogx(data1[:, 0], data1[:, 1], label="Dossier 1")
                ax[i].semilogx(data2[:, 0], data2[:, 1], label="Dossier 2")
            elif self.ui.logY.isChecked():
                ax[i].semilogy(data1[:, 0], data1[:, 1], label="Dossier 1")
                ax[i].semilogy(data2[:, 0], data2[:, 1], label="Dossier 2")
            else:
                ax[i].plot(data1[:, 0], data1[:, 1], label="Dossier 1")
                ax[i].plot(data2[:, 0], data2[:, 1], label="Dossier 2")

            if self.ui.grid.isChecked():
                ax[i].grid()
            try:
                ax[i].set_title(self.titles[i])
                ax[i].set_xlabel(self.xlabels[i])
                ax[i].set_ylabel(self.ylabels[i])
            except AttributeError:
                pass
        ax[0].legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def removeFolder(self):
        sender = self.sender()
        if sender.objectName() == "remove_1":
            self.init_vars_1()
        elif sender.objectName() == "remove_2":
            self.init_vars_2()
        self.plot()

def main():
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()