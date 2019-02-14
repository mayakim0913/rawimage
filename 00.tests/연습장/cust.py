from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import QMessageBox, QAction, qApp, QMenuBar
from PyQt5.QtGui import QIcon

from PyQt5.uic import loadUiType

import sys
import os

Ui_MainWindow, QMainWindow = loadUiType('first3.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
#        self.mayamenu(self)

        self.mayatoolbar()
        
    def mayatoolbar(self):
        self.toolbar = self.addToolBar('Save')

        save_action = QAction('$Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save program')

        exit_action = QAction('$Exit', self)
        exit_action.setShortcut('Ctrl+Z')
        exit_action.setStatusTip('Exit program')
        exit_action.triggered.connect(qApp.quit)

        self.toolbar.addAction(save_action)
        self.toolbar.addAction(exit_action)


#    def mayamenu(self):
#        mainMenu = self.menuBar()

#        menuBar = QMenuBar()
#        self.setMenuBar(menuBar)
#        file_menu.setNativeMenuBar(False)

#        file_menu = mainMenu.addMenu('&File')
#        exit2_action = QAction('&Exit', self)
#        exit2_action.setShortcut('Ctrl+Q')
#        exit2_action.setStatusTip('Exit program')
#        exit2_action_action.triggered.connect(qApp.quit)

if __name__ == '__main__':                                          
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main() 
    MainWindow.show()
    sys.exit(app.exec_())
