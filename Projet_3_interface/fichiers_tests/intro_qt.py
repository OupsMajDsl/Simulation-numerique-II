import sys
from PyQt5 import QtGui, QtWidgets

#https://www.tutorialspoint.com/pyqt/pyqt_signals_and_slots.htm
#https://build-system.fman.io/pyqt5-tutorial
#http://doc.qt.io/qt-5/qtwidgets-tutorials-addressbook-part6-example.html
#https://wiki.python.org/moin/PyQt/simple4
#http://zetcode.com/gui/pyqt4/firstprograms/

def window():
   app = QtWidgets.QApplication(sys.argv)
   widget = QtWidgets.QWidget()
   label = QtWidgets.QLabel(widget)
   label.setText("Hello World!")
   widget.setGeometry(100,100,200,50)
   label.move(50,20)
   widget.setWindowTitle("Interface")
   widget.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   window()