import sys, time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar

import numpy as np
import pylab as pl

import random


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.editLayout = QWidget()
        self.edit = QLineEdit('chfghfghf', self)
        self.edit.setDragEnabled(True)
        color = Qt.white
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.edit)

        self.editLayout.setLayout(self.left_layout)

        #Create the right layout that contains the plot canvas.    
        self.plotLayout = QWidget();

        canvas = Create_Canvas(self)       

        self.button = QPushButton('Plot')

        # set the layout
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(canvas)
        self.right_layout.addWidget(self.button)

        self.plotLayout.setLayout(self.right_layout)

        splitter_filebrowser = QSplitter(Qt.Horizontal)
        splitter_filebrowser.addWidget(self.editLayout)
        splitter_filebrowser.addWidget(self.plotLayout)
        splitter_filebrowser.setStretchFactor(1, 1)

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter_filebrowser)

        self.centralWidget().setLayout(hbox)

        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(750, 100, 600, 500)

class Create_Canvas(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        self.setAcceptDrops(True)

        figure = plt.figure()
        self.canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(self.canvas, self)
        toolbar.setStyleSheet("QComboBox { background-color: blue; }")
        t = self.palette()
        t.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(t)


        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(toolbar)
        self.right_layout.addWidget(self.canvas)

        # set the layout of this widget, otherwise the elements will not be seen.
        self.setLayout(self.right_layout)
        # plot some stuff
        self.ax = figure.add_subplot(111)
        self.ax.plot([1,2,5]) 
        self.ax.set_ylabel('Pouet')       
        # finally draw the canvas
        self.canvas.draw()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_() 