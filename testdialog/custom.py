from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *

import sys
import os

Ui_MainWindow, QMainWindow = loadUiType('testdialog.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

if __name__ == '__main__':                                          
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
#    width, height = screen_resolution.width()/1.5, screen_resolution.height()/1.2
    MainWindow = Main() 
#    MainWindow.resize(width,height)
    MainWindow.setWindowTitle('Image viewer by Maya')
    MainWindow.show()
    sys.exit(app.exec_())
