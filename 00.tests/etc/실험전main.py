#!/usr/bin/env python3
import sys
import os

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PIL import Image
from PIL.ImageQt import ImageQt

import numpy as np
from struct import *
import array
import cv2

from MainGUI import *
from LoadPicture import *

class MainWindow(QMainWindow, Ui_MainWindow):
    count = 0
    def __init__(self):
	QMainWindow.__init__(self)      
        self.setupUi(self)
        self.ConnectAction()

        self.filepath = 0
	self.format = 0
	self.imgwidth = 1920
	self.imgheight = 1080


    def ConnectAction(self):
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.actionSave_As.triggered.connect(self.SaveDialog)
        self.actionExit.triggered.connect(qApp.quit)
	self.actionZoom_in.triggered.connect(self.ReSizeSub)
	self.actionZoom_out.triggered.connect(self.ReSizeSub)

        self.comb_format.currentIndexChanged.connect(self.ChooseFormat)

        self.LineEdit_width.textEdited.connect(self.UpdateSize)
        self.LineEdit_height.textEdited.connect(self.UpdateSize)
        self.apply_button.clicked.connect(self.UYVY_clicked)

        self.pushbutton_autodetection.clicked.connect(self.Autobtn_clicked)


    def OpenDialog(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.filepath = self.fname
        self.statusbar.showMessage("Successfully Loaded: {}".format(self.fname))
        self.UYVY_clicked() 


    def SaveDialog(self):
        self.fname, _ = QFileDialog.getSaveFileName(self, 'Save file')
        self.statusbar.showMessage("Successfully saved: {}".format(self.fname))


    def UpdateSize(self):
        if self.LineEdit_width.text():
            self.imgwidth = int(self.LineEdit_width.text())
        elif self.LineEdit_height.text():
            self.imgheight = int(self.LineEdit_height.text())


    def ChooseFormat(self, i):
        print("wow")
        if i == 0:
            print "click index 0"
            self.format = 0
            print ("gloabal"+str(self.format))
            self.YUYV_clicked()
        elif i == 1:
            print "click index 1"
            self.format = 1
            print ("gloabal"+str(self.format))
            self.UYVY_clicked()
        elif i == 2:
            print "click index 2"
            self.format = 2
            print ("gloabal"+str(self.format))
            self.YVYU_clicked()
        elif i == 3:
            print "click index 3"
            self.format = 3
            print ("gloabal"+str(self.format))
            self.VYUY_clicked()

#######

    def YUYV_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.filepath
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
		y1 = ord(f_uyvy.read(1))                
		u  = ord(f_uyvy.read(1))
                y2 = ord(f_uyvy.read(1))
                v  = ord(f_uyvy.read(1))
                
                B = 1.164 * (y1-16) + 2.018 * (u - 128)
                G = 1.164 * (y1-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y1-16) + 1.596*(v - 128)
                pix[j*2, i] = int(R), int(G), int(B)

                B = 1.164 * (y2-16) + 2.018 * (u - 128) 
                G = 1.164 * (y2-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y2-16) + 1.596*(v - 128)
                pix[j*2+1, i] = int(R), int(G), int(B)

        data = image_out.tobytes('raw', "RGB")
        qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        pixmap = pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)
        self.LoadToSub(pixmap)

#######

    def UYVY_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
                u  = ord(f_uyvy.read(1))
                y1 = ord(f_uyvy.read(1))
                v  = ord(f_uyvy.read(1))
                y2 = ord(f_uyvy.read(1))
                
                B = 1.164 * (y1-16) + 2.018 * (u - 128)
                G = 1.164 * (y1-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y1-16) + 1.596*(v - 128)
                pix[j*2, i] = int(R), int(G), int(B)

                B = 1.164 * (y2-16) + 2.018 * (u - 128) 
                G = 1.164 * (y2-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y2-16) + 1.596*(v - 128)
                pix[j*2+1, i] = int(R), int(G), int(B)

        data = image_out.tobytes('raw', "RGB")
        qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        pixmap = pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)
        self.LoadToSub(pixmap)

#######

    def YVYU_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
		y1 = ord(f_uyvy.read(1))                
		v  = ord(f_uyvy.read(1))
                y2 = ord(f_uyvy.read(1))
                u  = ord(f_uyvy.read(1))
                
                B = 1.164 * (y1-16) + 2.018 * (u - 128)
                G = 1.164 * (y1-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y1-16) + 1.596*(v - 128)
                pix[j*2, i] = int(R), int(G), int(B)

                B = 1.164 * (y2-16) + 2.018 * (u - 128) 
                G = 1.164 * (y2-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y2-16) + 1.596*(v - 128)
                pix[j*2+1, i] = int(R), int(G), int(B)

        data = image_out.tobytes('raw', "RGB")
        qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        pixmap = pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)
        self.LoadToSub(pixmap)

#######

    def VYUY_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
		v = ord(f_uyvy.read(1))                
		y1  = ord(f_uyvy.read(1))
                u = ord(f_uyvy.read(1))
                y2  = ord(f_uyvy.read(1))
                
                B = 1.164 * (y1-16) + 2.018 * (u - 128)
                G = 1.164 * (y1-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y1-16) + 1.596*(v - 128)
                pix[j*2, i] = int(R), int(G), int(B)

                B = 1.164 * (y2-16) + 2.018 * (u - 128) 
                G = 1.164 * (y2-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
                R = 1.164 * (y2-16) + 1.596*(v - 128)
                pix[j*2+1, i] = int(R), int(G), int(B)

        data = image_out.tobytes('raw', "RGB")
        qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        pixmap = pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)
        self.LoadToSub(pixmap)

#######


    def LoadToSub(self, picture):
        MainWindow.count = MainWindow.count+1
        sub = QMdiSubWindow(self)
        loadPicture = LoadPicture(picture, sub)
        sub.setWidget(loadPicture)
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo"+str(MainWindow.count))
        self.mdiArea.addSubWindow(sub)
        sub.show()
	self.SetYUVchk()
        sub.resize(picture.size())
        loadPicture.log.MousePixmapSignal.connect(self.updatePixel)


    def ReSizeSub(self):
	self.scaleImage(1.25)


    def SetYUVchk(self):
        self.checkbox_y.setChecked(True)
        self.checkbox_u.setChecked(True)
        self.checkbox_v.setChecked(True)


    def updatePixel(self, point, color):
        self.UserInput_PixelValue_X.setText("{}".format(point.x()))
        self.UserInput_PixelValue_Y.setText("{}".format(point.y()))

        self.UserInput_PixelValue_R.setText("{}".format(color.red()))
        self.UserInput_PixelValue_G.setText("{}".format(color.green()))
        self.UserInput_PixelValue_B.setText("{}".format(color.blue()))


    def Autobtn_clicked(self):
        self.YUYV_clicked()
        self.UYVY_clicked()
        self.YVYU_clicked()
        self.VYUY_clicked()


if __name__ == '__main__':                                          
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    pyqtRemoveInputHook()

    app = QtWidgets.QApplication(sys.argv)
###
#    app.setAttribute(Qt.AA_EnableHighDpiScaling,True)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width()/1.5, screen_resolution.height()/1.2
###
    MainWindow = MainWindow() 
    MainWindow.setWindowTitle('Raw Image viewer')

    MainWindow.resize(width,height)

    MainWindow.show()
    sys.exit(app.exec_())




'''
        sub_size = self.pixmap
        print("1")
 
        sub_size.setWidth(sub_size.width() * 0.2)
        sub_size.setHeight(sub_size.height() * 0.2)
        print("2")
        self.pixmap = self.pixmap.scaled(sub_size, QtCore.Qt.KeepAspectRatio)
        print("3")
        self.update()



        widthSpinBox = QSpinBox()
        widthSpinBox.setRange(0, 1000)
        widthSpinBox.setSuffix(" %")
        heightSpinBox = QSpinBox()
        heightSpinBox.setRange(0, 1000)
        heightSpinBox.setSuffix(" %")

        from math import ceil
        image = self.mdiArea.sub.picture().toImage()
        widthZoom = ceil(image.width() * 100 / self.image.width())
        heightZoom = ceil(image.height() * 100 / self.image.height())
        widthSpinBox.setValue(widthZoom)
        heightSpinBox.setValue(heightZoom)
'''
