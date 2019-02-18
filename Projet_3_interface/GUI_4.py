import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QLabel, QCheckBox, QComboBox, 
                            QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QSpacerItem, QFrame)
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        # La fonction setGeometry prend en entrée les coordonnées x et y 
        # du coin gauche de la fenêtre (en partant du coin gauche de l'écran)
        TopLeftCorner_x = 500
        TopLeftCorner_y = 300
        # Dimensions de la fenêtre
        width = 1100
        height = 650
        # initialisation de la fenêtre:
        self.setGeometry(TopLeftCorner_x, TopLeftCorner_y, width, height) 
        # Fenêtre non redimensionnable
        self.setFixedSize(self.size())
        # Titre de la fenêtre 
        self.setWindowTitle('Interface tracé de données')
        # icone de la fenêtre dans la barre des tâches
        self.setWindowIcon(QIcon('icon.png'))

        # valeur par défaut du label de statut en bas de l'interface
        self.fileName = "no data loaded yet"
        # Valeur par défaut du type de tracé
        self.get_PlotType = "Temporel"

        # Initialisation des variables stockant les données à tracer
        self.data_init = np.zeros((1, 2))
        self.data = self.data_init
        self.MoreData = self.data_init

        # initialisation de l'interface: création d'une figure avec des axes vides
        # Figure nous permettra de tracer des figures avec plusieurs subplots par la suite 
        self.fig = Figure(figsize=(8, 5), dpi=100)
        ax = self.fig.add_subplot(111)
        self.fig.tight_layout()

        # Création de tous les objets de l'interface
        self.Objets()
        # Disposition des objets contenus dans la méthode Objets
        self.display()

        # Couleur d'arrière plan en blanc
        self.setAutoFillBackground(True)
        background_color = self.palette()       # création d'un objet palette qui stockera une couleur
        background_color.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(background_color)
    
    def Objets(self):
        # Intégration Matplotlib / PyQt 5
        # On choisit self.fig comme instance de FigureCanvas: les figures seront tracés
        # dans self.fig et le widget s'appelle self.canvas
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Bouton connecté à la méthode plot 
        self.LoadData = QPushButton('Charger')
        self.LoadData.setMaximumWidth(170)
        self.LoadData.clicked.connect(self.loadData)

        # Bouton connecté à "addPlot", tracer un 2e jeu de données
        self.AddData = QPushButton('+')
        self.AddData.setMaximumWidth(30)
        self.AddData.clicked.connect(self.loadMoreData)
        
        # Bouton pour actualiser le tracé
        self.F5 = QPushButton("Actualiser")
        self.F5.setMaximumWidth(115)
        self.F5.clicked.connect(self.plot)

        self.removeLastPlot = QPushButton("-")
        self.removeLastPlot.setMaximumWidth(30)
        self.removeLastPlot.clicked.connect(self.removePlot)

        # Label contenant le chemin du dernier fichier importé
        self.statusData = QLabel(self)
        self.statusData.setText(self.fileName)

        # Ajout d'un label de texte pour la liste des types de tracés
        # "Type de fichier chargé:"
        self.modetrace = QLabel(self)
        self.modetrace.setText("Type de fichier chargé:")

        # Création de la liste contenant tous les modes de tracé 
        self.Liste = QComboBox(self)
        self.Liste.setMaximumWidth(105)
        self.Liste.addItem("Temporel")
        self.Liste.addItem("FRF")
        self.Liste.addItem("Spectre")
        self.Liste.currentIndexChanged.connect(self.PlotType)

        # Ajout d'un label de texte pour les cases à cocher 
        # "Echelle en dB"
        self.echelledb = QLabel(self)
        self.echelledb.setText("Echelle en dB:")
        
        # Cases à cocher pour les axes en log
        self.dbx = QCheckBox(self)
        self.dbx.setText("X")
        self.dby = QCheckBox(self)
        self.dby.setText("Y")
        self.grid = QCheckBox(self)
        self.grid.setText("Quadrillage")

        #Ligne
        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.HLine)


    # Méthode qui gère la disposition des boutons sur l'interface
    # Disposition avec un layout pour simplifier le placement des boutons
    def display(self):
        # Distance en pixels de la séparation de chaque groupe d'objets
        sep = 50
        # Distance en pixels entre un label et l'objet suivant
        sep_lab = 7
        # Disposition de tous les éléments sur notre interface
        Vlayout = QVBoxLayout()
        # Element de matplotlib ajoutés au layout
        Vlayout.addWidget(self.toolbar)
        Vlayout.addWidget(self.canvas)

        # Création d'une grille pour afficher tous les boutons
        Glayout = QGridLayout()
        Glayout.setSpacing(0)       # Espace horizontal & vertical entre chaque case
        
        # 1ere ligne de boutons
        # Ajout des boutons Load et Add data
        DataLayout = QHBoxLayout()              # Création d'un groupe d'objets
        DataLayout.addWidget(self.LoadData)     # Ajout des widgets qu'on veut dans ce cadre
        DataLayout.addWidget(self.AddData)
        DataLayout.addStretch(1)
        Glayout.addLayout(DataLayout, 1, 0)

        # Ajout du label et de la liste pour le tracé
        TraceLayout = QHBoxLayout()
        TraceLayout.addWidget(self.modetrace)
        TraceLayout.addItem(QSpacerItem(sep_lab, 0))
        TraceLayout.addWidget(self.Liste)
        Glayout.addLayout(TraceLayout, 1, 1)

        Glayout.addItem(QSpacerItem(sep, 0), 1, 2)

        # Ajout du label et des cases à cocher pour l'affichage en log
        dbLayout = QHBoxLayout()
        dbLayout.addWidget(self.echelledb)
        dbLayout.addItem(QSpacerItem(sep_lab, 0))
        dbLayout.addWidget(self.dbx)
        dbLayout.addWidget(self.dby)

        dbLayout.addItem(QSpacerItem(sep, 0))
        dbLayout.addWidget(self.grid)
        Glayout.addLayout(dbLayout, 1, 3)

        # espace vertical entre les 2 rangées
        Glayout.addItem(QSpacerItem(0, 10), 2, 0)       # rangée 2 sert d'espacement
        
        # 2e rangée de boutons
        # Groupe des widgets pour actualiser la figure / enlever le plot supplémentaire
        managePlotLayout = QHBoxLayout()
        managePlotLayout.addWidget(self.F5)                 # bouton d'actualisation
        managePlotLayout.addWidget(self.removeLastPlot)     # enlever le dernier plot tracé
        managePlotLayout.addStretch(1)
        Glayout.addLayout(managePlotLayout, 3, 0)

        # On ajoute la grille au layout principal
        Vlayout.addLayout(Glayout)
        # En bas de cette grille, on ajoute une ligne séparatrice et le label de statut
        Vlayout.addWidget(self.sep)
        Vlayout.addWidget(self.statusData)
        # Le layout principal est mis sur Vlayout

        # cette commande ajoute tous les objets à la figure principale
        self.setLayout(Vlayout)

    # PlotType: FRF, temporel, ou spectre
    def PlotType(self):
        self.get_PlotType = self.Liste.currentText()
        print("Plot type selected = "+ self.get_PlotType)

    # Enlever le dernier plot tracé
    def removePlot(self):
        # on enlève les dernières données ...
        self.MoreData = self.data_init
        # ... et on retrace le plot
        self.plot()

    # Fonction pour ouvrir l'arboresence de fichiers
    def openFile(self):
        # Filtrer pour n'afficher que les fichiers en .txt piur éviter les erreurs
        filtre = "Text Files (*.txt)"
        try:
            # fileName contient le chemin absolu du fichier sélectionné
            fileName = QFileDialog.getOpenFileName(self, "Open File", "", filtre)[0]
            # On charge notre variable data avec le fichier voulu
            # on veut éviter que np.loadtxt retourne une erreur en essayant de charger l'en-tête
            # donc si on a une erreur, on passe une ligne de plus avec l'argument skiprows
            for i in range(0, 40):
                try:
                    data = np.loadtxt(fileName, skiprows=i)
                except ValueError:
                    pass
                # si on a pas d'erreur, on a bien passé l'en-tête, sans enlever de données
                # donc on arrête la boucle
                else:
                    break

            print("Successfully imported file "+fileName)
            # On affiche le chemin du fichier sur l'interface
            self.statusData.setText("File loaded --> "+fileName)
            return fileName, data
        # Si on ferme la boîte de dialogue avant sélection d'un fichier, apparition d'une OSError
        except OSError:
            pass

    def loadData(self):
        try:
            self.fileName, self.data = self.openFile()
            self.plot()
        # Si l'OSError apparaît dans la méthode openFile, alors self.data n'est pas défini
        # On ajoute alors une exception: aucun tracé ne sera réalisé si on n'a pas choisit de fichier
        except TypeError:
            pass

    # fonction identique à loadData mais qui gère le tracé secondaire sur l'interface
    def loadMoreData(self):
        try:
            self.fileName, self.MoreData = self.openFile()
            self.plot()
        # idem load data
        except TypeError:
            pass

    def plot(self):
        #reinitialiser le plot précédent
        self.fig.clear()
        # create an axis
        ax = self.fig.add_subplot(111)

        #Gestion du log
        if self.dbx.isChecked() and self.dby.isChecked():           # X et Y
            ax.loglog(self.data[:, 0], self.data[:, 1])
            ax.loglog(self.MoreData[:, 0], self.MoreData[:, 1])
        elif self.dbx.isChecked():                                  # X
            ax.semilogx(self.data[:, 0], self.data[:, 1])
            ax.semilogx(self.MoreData[:, 0], self.MoreData[:, 1])
        elif self.dby.isChecked():                                  # Y
            ax.semilogy(self.data[:, 0], self.data[:, 1])
            ax.semilogy(self.MoreData[:, 0], self.MoreData[:, 1])
        else:                                                       # linéaire
            ax.plot(self.data[:, 0], self.data[:, 1])
            ax.plot(self.MoreData[:, 0], self.MoreData[:, 1])
        # Option pour afficher une grille 
        if self.grid.isChecked():
            ax.grid()

        # Plusieurs types de tracés
        if self.get_PlotType == "Temporel":
            ax.set_xlabel("Temps [s]")
        elif self.get_PlotType == "Spectre":
            ax.set_xlabel("Fréquence [Hz]")
        ax.set_ylabel("Amplitude")

        if self.get_PlotType == "FRF":
            self.fig.delaxes(ax)
            self.fig.clear()
            ax1 = self.fig.add_subplot(211)
            ax2 = self.fig.add_subplot(212)
            ax1.plot(self.data[:, 0], self.data[:, 1])
            ax1.plot(self.MoreData[:, 0], self.MoreData[:, 1])
            try:
                ax2.plot(self.data[:, 0], self.data[:, 2])
                ax2.plot(self.MoreData[:, 0], self.MoreData[:, 2])
            except IndexError:
                pass
            ax2.set_xlabel("Fréquence [Hz]")
            ax1.set_ylabel("Module")
            ax2.set_ylabel("Phase")
            ax1.set_xticklabels([])
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    # création du cadre de la fenêtre
    app = QApplication(sys.argv)
    # appelle de la classe crée dans ce programme
    main = GUI()
    # affichage de la fenêtre
    main.show()
    # gestion de la fermeture de la fenêtre
    sys.exit(app.exec_())