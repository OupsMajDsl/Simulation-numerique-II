import sys 
from PyQt5 import QtGui, QtCore, QtWidgets 
class Example(QtWidgets.QWidget): 

    def __init__(self): 
        super(Example, self).__init__() 
        self.initUI() 

    def initUI(self): 

        self.Liste = QtWidgets.QComboBox(self) 
        
        self.Liste.addItems(
                'Sélectionner un fichier,--------,FRF_ModPhase,FRF_RealImage,Coherence,PowerSpectrum'.split(',')) 
        self.Liste.setCurrentIndex(0) 
        self.Liste.setToolTip('Select the legend position.') 
        self.Liste.currentIndexChanged[ 
        str].connect(self.avoid_db_change) 
        self.Liste.setMaximumWidth(170) 
        self.Liste.move(250, 50) 

        self.setGeometry(750, 300, 600, 400) 
        self.setWindowTitle('QtGui.QCheckBox') 
        self.show() 

    def avoid_db_change(self, text): 
        print("Processing {0} item".format(text)) 
        label = QtWidgets.QLabel(self)
        label.setText("Hello World!")
        label.move(50,20)
        self.Liste.blockSignals(True) 
        self.Liste.setCurrentIndex(0) 
        self.Liste.blockSignals(False) 


def main(): 
    app = QtWidgets.QApplication(sys.argv) 
    app.setWindowIcon(QtGui.QIcon('logo_univlemans.png'))
    ex = Example() 
    sys.exit(app.exec_()) 


if __name__ == '__main__': 
    main() 
