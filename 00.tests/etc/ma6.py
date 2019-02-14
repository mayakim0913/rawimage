from PyQt5 import QtGui, QtCore, QtWidgets, QtPrintSupport

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

#class myWindow(QtGui.QtWidgets):
#    def __init__(self, parent=None):
#        super(myWindow, self).__init__(parent)

class myWindow(QMainWindow):
    def __init__(self):
	QMainWindow.__init__(self)

        myLayout = QtWidgets.QVBoxLayout(self)
        Button = QtWidgets.QPushButton('Resize')
        myLayout.addWidget(Button)
        Button.setMinimumWidth(200)
        Button.clicked.connect(self.resizeDialog)

    def resizeDialog(self):
	self.animation = QtCore.QPropertyAnimation(self, "size")
	# self.animation.setDuration(1000) #Default 250ms
	if self.size().width()==200:
		self.animation.setEndValue(QtCore.QSize(600,300))
	else:
		self.animation.setEndValue(QtCore.QSize(200,100))
		self.animation.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('myApp')
    dialog = myWindow()
    dialog.resize(200,100)
    dialog.show()
    sys.exit(app.exec_())
