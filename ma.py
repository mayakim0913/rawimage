#!/usr/bin/env python3
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *

import sys
import os

from second import Ui_MainWindow

########
from PIL import Image
from PIL.ImageQt import ImageQt
from struct import *
import array

import numpy as np
import cv2
########

#from GraphicsArea_GUI import *

#from second import *

######################################################
########################################################
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setUpMainUiFunction()

    def setUpMainUiFunction(self):
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.actionExit.triggered.connect(qApp.quit)

    def OpenDialog(self):
        width = 1920
        height = 1080

        IMG_NAME = 'UYVY_little_1920x1080.raw'
        f_uyvy = open(IMG_NAME, "rb")

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
                u  = ord(f_uyvy.read(1));
                y1 = ord(f_uyvy.read(1));
                v  = ord(f_uyvy.read(1));
                y2 = ord(f_uyvy.read(1));

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
        self.label.setPixmap(pixmap)
'''
	y = array.array('B') #initialization 8bits
	u = array.array('B') #initialization 8bits -> /2
	v = array.array('B') #initialization 8bits -> /2
'''
#        self.label.setPixmap(QPixmap.fromImage(ImageQt(image_out)).scaled(width,height))
#        image_out.show()
'''
        im = ImageQt(image_out)
#	im2 = QtGui.QImage(im)
	pixmap = QtGui.QPixmap.fromImage(im)
        self.label.resize(width, height)
        self.label.setPixmap(pixmap)
'''

##########################################################
##########################################################
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle('Image viewer by Maya')
#    screen_resolution = app.desktop().screenGeometry()
#    width, height = screen_resolution.width()/1.5, screen_resolution.height()/1.2
#    MainWindow.resize(width,height)
    MainWindow.show()
    sys.exit(app.exec_())
