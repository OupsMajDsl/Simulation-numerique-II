import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtCore, QtGui

class WidgetPlot(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        # Création d'un layout vertical dans l'interface
        self.setLayout(QtWidgets.QVBoxLayout())
        # On appelle la classe qui crée l'ensemble de la figure
        self.canvas = PlotCanvas(self, width=10, height=8)
        # On appelle la toolbar de matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        # On ajoute les 2 widgets à l'interface
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) 
        
    #Initialisation d'un plot vide
    def initPlot(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([], [])
        self.ax.set_title('')
    
    def delPlot(self):
        try:
            self.fig.delaxes(self.ax)
        except (NameError, AttributeError):
            pass
        try:
            self.fig.delaxes(self.ax1)
            self.fig.delaxes(self.ax2)
        except (NameError, AttributeError):
            pass
        self.toolbar.update()

    #Tracé avec les différents modes
    def plot(self, data, mode, dbx, dby):
        self.fig.clear()
        self.toolbar.update()
        if mode == "Temps":
            tps = data[:, 0]
            amp = data[:, 1]
            ax1 = self.figure.add_subplot(111)
            if dbx:
                ax1.semilogx(tps, amp)
            elif dbx and dby:
                ax1.loglog(tps, amp)
            elif dby:
                ax1.semilogy(tps, amp)
            else:
                ax1.plot(tps, amp)
            ax1.set_xlabel("Temps")
            ax1.set_ylabel("Amplitude")
            ax1.set_title("Tracé temporel")
        if mode == "Spectre":
            fq = data[:, 0]
            amp = data[:, 1]
            ax1 = self.figure.add_subplot(111)
            ax1.plot(fq, amp)
            ax1.set_xlabel("Fréquence")
            ax1.set_ylabel("Amplitude")
            ax1.set_title("Spectre")
        if mode == "FRF":
            fq = data[:, 0]
            mod = data[:, 1]
            phas = data[:, 2]
            ax1 = self.figure.add_subplot(211)
            ax2 = self.figure.add_subplot(212)
            ax1.plot(fq, mod)
            ax2.plot(fq, phas)
            ax1.set_title('Module')
            ax2.set_title('Phase')

        self.fig.tight_layout()
        self.show()


class GUI(QtWidgets.QMainWindow): 
    def __init__(self): 
        super(GUI, self).__init__()
        #Variables
        self.data = np.ndarray((1, 5))
        self.init_fileName = "No data loaded yet" 
        self.fileName = self.init_fileName
        self.modetrace = "Temps"
        self.dbx = False
        self.dby = False
        #Initialize the window
        self.setGeometry(750, 300, 800, 500) 
        self.setWindowTitle('Interface Analyseur CTTM')
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        #Background color to white
        self.setAutoFillBackground(True)
        back_color = self.palette()
        back_color.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(back_color)
        #Load all the elements
        self.initUI()

    def initUI(self): 
        # Appelle à la classe WidgetPlot qui crée la toolbar et l'ensemble de la figure
        self.widget_plot = WidgetPlot(self)
        self.widget_plot.canvas.initPlot()
        self.ListeTrace()
        self.objects()

        self.Display()
        self.show()

#####################################################################
                        #Chargement donnée et tracé
#####################################################################
    def plotData(self):
        # self.widget_plot.canvas.delPlot()
        if self.checkDB_x.isChecked():
            print('dB_x')
            self.dbx = True
        if self.checkDB_y.isChecked():
            print('dB_y')
            self.dby = True
        self.widget_plot.canvas.plot(self.data, self.modetrace, self.dbx, self.dby)

    def openFile(self):
        filtre = "Text Files (*.txt)"
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget(), "Open File", "", filtre)[0]
        self.data = np.loadtxt(self.fileName, skiprows=1)
        print("Successfully imported file "+self.fileName)
        self.statusData.setText("File loaded --> "+self.fileName)
        self.plotData()


#####################################################################
                        #Interface
#####################################################################
    def ListeTrace(self):
        self.labelListe = QtWidgets.QLabel(self)
        self.labelListe.setText('Sélectionner un type de tracé')
        self.Liste = QtWidgets.QComboBox(self)
        self.Liste.addItem("Temps")
        self.Liste.addItem("FRF")
        self.Liste.addItem("Spectre")
        def mode_de_trace():
            self.modetrace = self.Liste.currentText()
            print("Mode de tracé sélectionné: {}".format(self.modetrace))
        self.Liste.setCurrentIndex(0) 
        self.Liste.setToolTip('Sélectionner le type de signal à tracer') 
        self.Liste.setMaximumWidth(170)
        self.Liste.currentIndexChanged.connect(mode_de_trace)


    def objects(self):
        """ Objets contenus dans l'interface"""

        self.checkDB_x = QtWidgets.QCheckBox(self)
        self.checkDB_x.setText('dB - X axis')
        self.checkDB_y = QtWidgets.QCheckBox(self)
        self.checkDB_y.setText('dB - Y axis')

        self.loadBtn = QtWidgets.QPushButton("Load Data")
        self.loadBtn.setMaximumWidth(100)
        self.loadBtn.clicked.connect(self.openFile)

        self.statusData = QtWidgets.QLabel(self)
        self.statusData.setText(self.fileName)



    def Display(self):
        """Building the GUI"""
        vertic_lay = QtWidgets.QVBoxLayout(self.central_widget)
        vertic_lay.addWidget(self.widget_plot)

        horiz_lay = QtWidgets.QHBoxLayout()
        vertic_lay.addLayout(horiz_lay)
        horiz_lay.addWidget(self.labelListe)

        horiz_lay_2 = QtWidgets.QHBoxLayout()
        vertic_lay.addLayout(horiz_lay_2)
        horiz_lay_2.addWidget(self.Liste)
        horiz_lay_2.addWidget(self.checkDB_x)
        horiz_lay_2.addWidget(self.checkDB_y)

        vertic_lay.addItem(QtWidgets.QSpacerItem(0, 20))

        horiz_lay_3 = QtWidgets.QHBoxLayout()
        vertic_lay.addLayout(horiz_lay_3)

        horiz_lay_3.addWidget(self.loadBtn)
        horiz_lay_3.addWidget(self.statusData)


#####################################################################
                        #Exécution de l'app
#####################################################################
def main(): 
    app = QtWidgets.QApplication(sys.argv) 
    gui = GUI() 
    # GUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()