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
from math import ceil

from LoadPicture import *

things = os.path.dirname(os.path.abspath(__file__))
l = lambda f: os.path.join(things, f)


class MainWindow(QMainWindow):
    count = 0
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi(l('MainGUI.ui'), self)
        self.ActionIcon()
        self.ConnectAction()

        self.filepath = None
        self.format = 1
        self.imgwidth = 1920
        self.imgheight = 1080
        self.scaleFactor = 1.0
        self.pix = None

    def ActionIcon(self):
        icon_open = QIcon()
        icon_save = QIcon()
        icon_zoomin = QIcon()
        icon_zoomout = QIcon()
        icon_help = QIcon()
        icon_about = QIcon()
        icon_exit = QIcon()

        icon_open.addPixmap(QPixmap('open.png'))
        icon_save.addPixmap(QPixmap('save.png'))
        icon_zoomin.addPixmap(QPixmap('zoomin.png'))
        icon_zoomout.addPixmap(QPixmap('zoomout.png'))
        icon_help.addPixmap(QPixmap('help.png'))
        icon_about.addPixmap(QPixmap('about.png'))
        icon_exit.addPixmap(QPixmap('exit.png'))

        self.actionOpen.setIcon(icon_open)
        self.actionSave_As.setIcon(icon_save)
        self.actionZoom_in.setIcon(icon_zoomin)
        self.actionZoom_out.setIcon(icon_zoomout)
        self.actionHelp.setIcon(icon_help)
        self.actionAbout.setIcon(icon_about)
        self.actionExit.setIcon(icon_exit)


    def ConnectAction(self):
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.actionSave_As.triggered.connect(self.SaveDialog)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionZoom_in.triggered.connect(self.ZoomIn)
        self.actionZoom_out.triggered.connect(self.ZoomOut)

        self.comb_format.currentIndexChanged.connect(self.ChooseFormat)

        self.checkbox_y.stateChanged['int'].connect(self.MatchFormat)
	self.checkbox_u.stateChanged['int'].connect(self.MatchFormat)
        self.checkbox_v.stateChanged['int'].connect(self.MatchFormat)
        self.checkbox_swap.stateChanged['int'].connect(self.SwapFormat)

        #self.radiobutton_be.clicked.connect(self.ChangeE)
        #self.radiobutton_le.clicked.connect(self.ChangeE)

        self.LineEdit_width.textEdited.connect(self.UpdateSize)
        self.LineEdit_height.textEdited.connect(self.UpdateSize)
        self.apply_button.clicked.connect(self.MatchFormat)

        self.pushbutton_autodetection.clicked.connect(self.Autobtn_clicked)


    def OpenDialog(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.filepath = self.fname
        self.statusbar.showMessage("Successfully Loaded: {}".format(self.fname))

        self.checkbox_y.setChecked(True)
        self.checkbox_u.setChecked(True)
        self.checkbox_v.setChecked(True)

        self.radiobutton_le.setChecked(True)

        self.ot_clicked()
	self.label_img.setPixmap(self.pix)


    def SaveDialog(self):
        self.fname, _ = QFileDialog.getSaveFileName(self, 'Save file')
        self.statusbar.showMessage("Successfully saved: {}".format(self.fname))


    def ChooseFormat(self, i):
        print("wow")
        if i == 0:
            self.format = 0
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)
        elif i == 1:
            self.format = 1
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)
        elif i == 2:
            self.format = 2
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)
        elif i == 3:
            self.format = 3
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)


    def MatchFormat(self):
        if self.format == 0:
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 1:
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 2:
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 3:
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)



    def SwapFormat(self):
        if self.format == 0:
            self.format = 2
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 1:
            self.format = 3
            self.tf_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 2:
            self.format = 0
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)
        elif self.format == 3:
            self.format = 1
            self.ot_clicked()
            self.label_img.setPixmap(self.pix)


    def yuv_clicked(self, y1, y2, u_b, u_g, v_g, v_r, pix, i, j):
            B = y1 + u_b
            G = y1 + v_g + u_g
            R = y1 + v_r
            pix[j*2, i] = int(R), int(G), int(B)

            B = y2 + u_b
            G = y2 + v_g + u_g
            R = y2 + v_r
            pix[j*2+1, i] = int(R), int(G), int(B)


    def ot_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
        f_uyvy = open(IMG_NAME)

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):
		if self.format == 0:
	                y1 = ord(f_uyvy.read(1))
	                u  = ord(f_uyvy.read(1))
	                y2 = ord(f_uyvy.read(1))
			v  = ord(f_uyvy.read(1))

		elif self.format == 1:
	                u  = ord(f_uyvy.read(1))
	                y1 = ord(f_uyvy.read(1))
	                v  = ord(f_uyvy.read(1))
	                y2 = ord(f_uyvy.read(1))

		y1 = 1.164 * (y1-16)
		u_b = 2.018 * (u - 128)
		u_g = - 0.391 * (u - 128)
		y2 = 1.164 * (y2-16)
                v_g = - 0.813 * (v - 128)
                v_r = 1.596 * (v - 128)


		if self.checkbox_y.isChecked() == False:
	                y1 = 0
	                y2 = 0
		if self.checkbox_u.isChecked() == False:
	                u_b  = 0
	                u_g  = 0
		if self.checkbox_v.isChecked() == False:
	                v_g = 0
	                v_r = 0

		self.yuv_clicked(y1, y2, u_b, u_g, v_g, v_r, pix, i, j)


	data = image_out.tobytes('raw', "RGB")
	qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
	pixmap = QtGui.QPixmap.fromImage(qim)
	self.pix = pixmap


    def tf_clicked(self):
        width = self.imgwidth
        height = self.imgheight

        IMG_NAME = self.fname
        f_uyvy = open(IMG_NAME)

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()

        for i in range(0,height):
            for j in range(0, int(width/2)):

		if self.format == 2:
			y1 = ord(f_uyvy.read(1))
			v  = ord(f_uyvy.read(1))
	                y2 = ord(f_uyvy.read(1))
	                u  = ord(f_uyvy.read(1))
		elif self.format == 3:
			v = ord(f_uyvy.read(1))
			y1  = ord(f_uyvy.read(1))
	                u = ord(f_uyvy.read(1))
	                y2  = ord(f_uyvy.read(1))

		y1 = 1.164 * (y1-16)
		u_b = 2.018 * (u - 128)
		u_g = - 0.391 * (u - 128)
		y2 = 1.164 * (y2-16)
                v_g = - 0.813 * (v - 128)
                v_r = 1.596 * (v - 128)



		if self.checkbox_y.isChecked() == False:
	                y1 = 0
	                y2 = 0
		if self.checkbox_v.isChecked() == False:  #matter!
	                u_b  = 0
	                u_g  = 0
		if self.checkbox_u.isChecked() == False:  #matter!
	                v_g = 0
	                v_r = 0

		self.yuv_clicked(y1, y2, u_b, u_g, v_g, v_r, pix, i, j)

        data = image_out.tobytes('raw', "RGB")
        qim = QtGui.QImage(data, image_out.size[0], image_out.size[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        self.pix = pixmap



    def LoadToSub(self, picture):
        MainWindow.count = MainWindow.count+1

        sub = QMdiSubWindow(self)
        loadPicture = LoadPicture(picture, sub)

        sub.setWidget(loadPicture)
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo"+str(MainWindow.count))
        self.mdiArea.addSubWindow(sub)

        sub.show()
        sub.resize(500,500)
        loadPicture.log.MousePixmapSignal.connect(self.updatePixel)


    def updatePixel(self, point, color):
        self.UserInput_PixelValue_X.setText("{}".format(point.x()))
        self.UserInput_PixelValue_Y.setText("{}".format(point.y()))

        self.UserInput_PixelValue_R.setText("{}".format(color.red()))
        self.UserInput_PixelValue_G.setText("{}".format(color.green()))
        self.UserInput_PixelValue_B.setText("{}".format(color.blue()))


    def Autobtn_clicked(self):
        self.YUYV_clicked()
        self.LoadToSub(self.pix)
        self.UYVY_clicked()
        self.LoadToSub(self.pix)
        self.YVYU_clicked()
        self.LoadToSub(self.pix)
        self.VYUY_clicked()
        self.LoadToSub(self.pix)


    def UpdateSize(self):
        if self.LineEdit_width.text():
            self.imgwidth = int(self.LineEdit_width.text())
        elif self.LineEdit_height.text():
            self.imgheight = int(self.LineEdit_height.text())


    def ZoomIn(self):
        self.scaleFactor += 0.1
        self.label_img.setPixmap(self.pix.scaled(int(self.imgwidth*self.scaleFactor),int(self.imgheight*self.scaleFactor),QtCore.Qt.KeepAspectRatio))


    def ZoomOut(self):
        self.scaleFactor -= 0.1
        self.label_img.setPixmap(self.pix.scaled(int(self.imgwidth*self.scaleFactor),int(self.imgheight*self.scaleFactor),QtCore.Qt.KeepAspectRatio))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle('Raw Image viewer')
    MainWindow.show()
    sys.exit(app.exec_())

