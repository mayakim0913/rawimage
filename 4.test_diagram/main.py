#!/usr/bin/env python3

# Import modules
from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys
import os

# Directory where all the things are
things = os.path.dirname(os.path.abspath(__file__))
l = lambda f: os.path.join(things, f)

# QApplication instance
app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = uic.loadUi(l('test.ui'), self)
        self.ui.show()


window = MainWindow()
app.exec_()
