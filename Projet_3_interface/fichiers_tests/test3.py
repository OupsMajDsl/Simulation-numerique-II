import sys
from random import randrange
import matplotlib
#matplotlib.use("Qt5Agg")
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QLabel, QLineEdit, QPushButton)
 
 
class MainWindow(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        super(MainWindow, self).__init__(fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.setFixedSize(self,400,400)
        timer = QTimer(self)
        self.setWindowTitle("Mesures")
        timer.timeout.connect(self.update_figure)
 
    def update_figure(self):
        pass
 
class MyDynamicMplCanvas(MainWindow):
    a=2
    liste_x=[0,0]
    liste_y=[0,0]
    tstart=time.time()
    def __init__(self, *args, **kwargs):
        MainWindow.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(250)
 
    def update_figure(self):
        self.a=self.a+1
        self.liste_x.extend([self.a])
        self.liste_y.extend([randrange(0,5)])
        self.axes.plot(self.liste_x, self.liste_y)
        #self.axes.axis([0,250,0,6])
        print(time.time()-self.tstart)
        self.draw()
 
class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.main_widget = QWidget(self)
 
        layout1 = QVBoxLayout(self.main_widget)
        layout2 = QHBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.bouton1=QPushButton()
        self.bouton2=QPushButton()
        self.bouton3=QPushButton()
        layout1.addLayout(layout2)
 
        layout1.addWidget(self.bouton1)
        layout2.addWidget(self.bouton2)
        layout2.addWidget(self.bouton3)
        layout2.addWidget(dc)
 
 
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
 
    def fileQuit(self):
        self.close()
 
    def closeEvent(self, ce):
        self.fileQuit()
 
    def about(self):
        QMessageBox.about(self, "About",)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("PyQt5 Matplot Example")
    aw.show()
    app.exec_()
