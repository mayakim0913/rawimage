import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from MainGUI import *
from main import *


class ConvertFixel(QWidget):
    def __init__(self, __filepath, __format, __imgwidth, __imgheight):
        self.filepath = __filepath
        self.form = __format
        self.width =  __imgwidth
        self.height = __imgheight
        self.__func = None
        self.choice_func()

    def choice_func(self):
        if self.form == 0:
            self.__func = self.YUYV_clicked()
        elif self.form == 1:
            self.__func = self.UYVY_clicked()
        elif self.form == 2:
            self.__func = self.YVYU_clicked()
        elif self.form == 3:
            self.__func = self.VYUY_clicked()


###############################
    def YUYV_clicked(self):
        wid = self.width
        hei = self.height

        IMG_NAME = self.filepath
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (wid, hei))
        pix = image_out.load()

        for i in range(0,hei):
            for j in range(0, int(wid/2)):
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
        return pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)

#######

    def UYVY_clicked(self):
        wid = self.width
        hei = self.height

        IMG_NAME = self.filepath
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (wid, hei))
        pix = image_out.load()

        for i in range(0,hei):
            for j in range(0, int(wid/2)):
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
        return pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)

#######

    def YVYU_clicked(self):
        wid = self.width
        hei = self.height

        IMG_NAME = self.filepath
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (wid, hei))
        pix = image_out.load()

        for i in range(0,hei):
            for j in range(0, int(wid/2)):
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
        return pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)

#######

    def VYUY_clicked(self):
        wid = self.width
        hei = self.height

        IMG_NAME = self.filepath
        f_uyvy = open(IMG_NAME) #"rb"

        image_out = Image.new("RGB", (wid, hei))
        pix = image_out.load()

        for i in range(0,hei):
            for j in range(0, int(wid/2)):
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
        return pixmap #.scaled(1000,1000,QtCore.Qt.KeepAspectRatio)

#######


'''

    def ChooseFormat(self, i):
        print("wow")
        if i == 0:
            print "click index 0"
            self.YUYV_clicked()
        elif i == 1:
            print "click index 1"
            self.UYVY_clicked()
        elif i == 2:
            print "click index 2"
            self.YVYU_clicked()
        elif i == 3:
            print "click index 3"
            self.VYUY_clicked()

       # format = self.comb_format.currentIndexx
       # if format == 0:
       #     print("first one clicked")

       # self.comb_format.currentIndex
       # lambda: self.combo_box.setCurrentIndex(3)
#######

    def YUYV_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
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
'''
