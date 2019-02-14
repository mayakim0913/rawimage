from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *

import sys
import os

from GraphicsArea_GUI import *
from loadPicture import *



Ui_MainWindow, QMainWindow = loadUiType('first2.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

        self.mayatoolbar()
        self.pushbutton_autodetection.clicked.connect(self.btn_clicked)
        
    def mayatoolbar(self):
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setStatusTip('Open image')
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.toolBar.addAction(self.actionOpen)

        self.actionSave_AS.setShortcut('Ctrl+S')
        self.actionSave_AS.setStatusTip('Save image')
        self.actionSave_AS.triggered.connect(self.save_image_but)
        self.toolBar.addAction(self.actionSave_AS)

        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Close program')
        self.actionExit.triggered.connect(qApp.quit)
        self.toolBar.addAction(self.actionExit)

        self.actionZoom_In.setShortcut('Ctrl+=')
        self.actionZoom_In.setStatusTip('Zoom in image 25%')
#        self.actionZoom_In.triggered.connect(self.scaleImage(1.25))
        self.toolBar.addAction(self.actionZoom_In)

        self.actionZoom_out.setShortcut('Ctrl+-')
        self.actionZoom_out.setStatusTip('Zoom out image 25%')
#        self.actionZoom_out.triggered.connect(self.scaleImage(0.8))
        self.toolBar.addAction(self.actionZoom_out)

    def OpenDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        PicturePath = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open File", PicturePath, "PNG File (*.png)", options=options)
    
        for filename in filenames:
            pixmap = QPixmap(filename)
            self.showPicture(pixmap)
            self.statusbar.showMessage("Successfully Loaded: {}".format(filename))

    
    def showPicture(self, picture):
        sub = QtWidgets.QMdiSubWindow(self)
        loadPicture = LoadPicture(picture, sub)
       
        sub.setWidget(loadPicture)
        
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo")
        self.mdiArea.addSubWindow(sub)
        
        sub.show()
        
        sub.resize(picture.size())
        
        loadPicture.log.MousePixmapSignal.connect(self.updatePixel)


    def updatePixel(self, point, color):
        self.UserInput_PixelValue_X.setText("{}".format(point.x()))
        self.UserInput_PixelValue_Y.setText("{}".format(point.y()))

        self.UserInput_PixelValue_R.setText("{}".format(color.red()))
        self.UserInput_PixelValue_G.setText("{}".format(color.green()))
        self.UserInput_PixelValue_B.setText("{}".format(color.blue()))


    def save_image_but(self):
        self.fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')

#        QFileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)


    def btn_clicked(self):
        QMessageBox.about(self, "message", "yet to be develop:)")




if __name__ == '__main__':                                          
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
#    width, height = screen_resolution.width()/1.5, screen_resolution.height()/1.2
    MainWindow = Main() 
#    MainWindow.resize(width,height)
    MainWindow.setWindowTitle('Image viewer by Maya')
    MainWindow.show()
    sys.exit(app.exec_())

