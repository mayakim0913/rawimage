from PyQt5 import QtGui, QtCore, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import urllib
import sys


class MainWindow(QMainWindow):
    def __init__(self):
	QMainWindow.__init__(self)
#        super(myApplication, self).__init__()
        #---- Prepare a Pixmap ----
        url = ('http://sstatic.net/stackexchange/img/logos/' +
               'careers/careers-icon.png?v=0288ba302bf6')
        self.img = QtGui.QImage()
        self.img.loadFromData(urllib.urlopen(url).read())

        pixmap = QtGui.QPixmap(self.img)

        #---- Embed Pixmap in a QLabel ----

        diag = (pixmap.width()**2 + pixmap.height()**2)**0.5

        self.label =  QtWidgets.QLabel()
        self.label.setMinimumSize(diag, diag)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(pixmap)

        #---- Prepare a Layout ----

        grid = QtWidgets.QGridLayout()

        button = QtWidgets.QPushButton('Rotate 15 degrees')
        button.clicked.connect(self.rotate_pixmap)

        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

        self.setLayout(grid)

        self.rotation = 0

    def rotate_pixmap(self):

        #---- rotate ----

        # Rotate from initial image to avoid cumulative deformation from
        # transformation

        pixmap = QtGui.QPixmap(self.img)
        self.rotation += 15

        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----

        self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = MainWindow()  
    instance.show()    
    sys.exit(app.exec_())

