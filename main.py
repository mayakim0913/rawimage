#!/usr/bin/env python3
import sys
import os

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from PIL import Image
from PIL.ImageQt import ImageQt

import numpy as np
from struct import *
import array
import cv2

from MainGUI import *
from LoadPicture import *
#LogObject, LoadPicture, PictureItem, ConvertFixel


class MainWindow(QMainWindow, Ui_MainWindow):
    count = 0

    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.ConnectAction()

        self.filepath = 0
	self.format = 0
	self.imgwidth = 1920
	self.imgheight = 1080


    def ConnectAction(self):
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.actionExit.triggered.connect(qApp.quit)

        self.comb_format.currentIndexChanged.connect(self.ChooseFormat)

        self.LineEdit_width.textEdited.connect(self.UpdateSize)
        self.LineEdit_height.textEdited.connect(self.UpdateSize)
        self.apply_button.clicked.connect(self.UYVY_clicked) #######fix it!!!!!

        self.pushbutton_autodetection.clicked.connect(self.Autobtn_clicked)


    def OpenDialog(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.filepath = self.fname
        self.statusbar.showMessage("Successfully Loaded: {}".format(self.fname))
        self.UYVY_clicked() #######fix it!!!!!!!


    def UpdateSize(self):
        if self.LineEdit_width.text():
            self.imgwidth = int(self.LineEdit_width.text())
        elif self.LineEdit_height.text():
            self.imgheight = int(self.LineEdit_height.text())

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


    def ChooseFormat(self, i):
        print("wow")

        if i == 0:
            print "click index 0"
            self.format = 0
            print ("gloabal"+str(self.format))
        elif i == 1:
            print "click index 1"
            self.format = 1
            print ("gloabal"+str(self.format))
        elif i == 2:
            print "click index 2"
            self.format = 2
            print ("gloabal"+str(self.format))
        elif i == 3:
            print "click index 3"
            self.format = 3
            print ("gloabal"+str(self.format))

        __filepath = self.filepath
	__format = self.format
	__imgwidth = self.imgwidth
	__imgheight = self.imgheight

        pixmap = ConvertFixel(__filepath, __format, __imgwidth, __imgheight)
        self.LoadToSub(pixmap)


    def LoadToSub(self, picture):
        MainWindow.count = MainWindow.count+1
        sub = QMdiSubWindow(self)
        loadPicture = LoadPicture(picture, sub)
        sub.setWidget(loadPicture)
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo"+str(MainWindow.count))
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


    def Autobtn_clicked(self):
        QMessageBox.about(self, "message", "yet to be develop:)")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle('Raw Image viewer')
    MainWindow.show()
    sys.exit(app.exec_())
