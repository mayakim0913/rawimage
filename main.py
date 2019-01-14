#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disble=missing-docstring
#pylint:disable=no-name-in-module
"""

This script converts raw image to other image format
Form implementation generated from reading ui file 'widget.ui'
python: 3.6

"""
import sys
import os

from enum import Enum, IntEnum
from PyQt5 import (Qt, QtCore, QtGui, QtWidgets, uic)
from PyQt5.uic import loadUi

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PIL import Image


from LoadPicture import *
import Parser


THINGS = os.path.dirname(os.path.abspath(__file__))
L = lambda f: os.path.join(THINGS, f)


class YUVFormat(IntEnum):
    YUYV_LE = 1
    UYVY_LE = 2
    YVYU_LE = 3
    VYUY_LE = 4

    YUYV_BE = 5
    UYVY_BE = 6
    YVYU_BE = 7
    VYUY_BE = 8


class RGBFormat(IntEnum):
    BGR3_LE = 11
    RGB3_LE = 12
    XR24_LE = 13
    RGBP_LE = 14

    BGR3_BE = 15
    RGB3_BE = 16
    XR24_BE = 17
    RGBP_BE = 18


class MainWindow(QMainWindow):
    count = 0
    def __init__(self):
        QMainWindow.__init__(self)
        self.pyqt_ui = uic.loadUi(L('MainGUI.ui'), self)
        self.action_icon()
        self.connect_action()

        self.filepath = None
        self.format = 1
        self._format = 1
        self.imgwidth = 400
        self.imgheight = 400
        self.factor = 1.0
        self.pix = None


    def action_icon(self):
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


    def connect_action(self):
        self.actionOpen.triggered.connect(self.open_dialog)
        self.actionSave_As.triggered.connect(self.save_dialog)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)

        self.comb_format.currentIndexChanged.connect(self.set_format)

        self.checkbox_y.clicked.connect(self.asign_format)
        self.checkbox_u.clicked.connect(self.asign_format)
        self.checkbox_v.clicked.connect(self.asign_format)
        self.checkbox_r.clicked.connect(self.asign_format)
        self.checkbox_g.clicked.connect(self.asign_format)
        self.checkbox_b.clicked.connect(self.asign_format)
        self.checkbox_swap.clicked.connect(self.swap_format)

        self.radiobutton_be.clicked.connect(self.match_format)
        self.radiobutton_le.clicked.connect(self.match_format)

        self.LineEdit_width.textEdited.connect(self.update_size)
        self.LineEdit_height.textEdited.connect(self.update_size2)
        self.apply_button.clicked.connect(self.asign_format)

        self.pushbutton_autodetection.clicked.connect(self.auto_detect)


    def open_dialog(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.filepath = self.fname
        self.statusbar.showMessage("Successfully Loaded: {}".format(self.fname))
        self.radiobutton_le.setChecked(True)


        if self.format > 0 and self.format < 9:
            self.group_yuv.setEnabled(True)
            self.group_rgb.setEnabled(False)

            self.checkbox_y.setChecked(True)
            self.checkbox_u.setChecked(True)
            self.checkbox_v.setChecked(True)

            self.checkbox_r.setChecked(False)
            self.checkbox_g.setChecked(False)
            self.checkbox_b.setChecked(False)


        elif self.format > 10 and self.format < 19:
            self.group_yuv.setEnabled(False)
            self.group_rgb.setEnabled(True)

            self.checkbox_r.setChecked(True)
            self.checkbox_g.setChecked(True)
            self.checkbox_b.setChecked(True)

            self.checkbox_y.setChecked(False)
            self.checkbox_u.setChecked(False)
            self.checkbox_v.setChecked(False)
            self.checkbox_swap.setChecked(False)


        self.asign_format()



    def save_dialog(self):
        self.fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '', '*.png')
        self.filepath = self.fname
        pixmap = self.pix
        obj = pixmap.toImage()
        obj.save(self.filepath, "PNG")
        self.statusbar.showMessage("Successfully saved: {}".format(self.fname))



    def checkbox_state(self):
        before_format = self._format
        current_format = self.format

        before_group = int(before_format/10)
        current_group = int(current_format/10)

        if self.format > 0 and self.format < 9:
            self.group_yuv.setEnabled(True)
            self.group_rgb.setEnabled(False)
        elif self.format > 10 and self.format < 19:
            self.group_yuv.setEnabled(False)
            self.group_rgb.setEnabled(True)

        if before_group != current_group:
            if current_group == 0:
                self.checkbox_y.setChecked(True)
                self.checkbox_u.setChecked(True)
                self.checkbox_v.setChecked(True)

                self.checkbox_r.setChecked(False)
                self.checkbox_g.setChecked(False)
                self.checkbox_b.setChecked(False)
                self.checkbox_swap.setChecked(False)
            elif current_group == 1:
                self.checkbox_y.setChecked(False)
                self.checkbox_u.setChecked(False)
                self.checkbox_v.setChecked(False)

                self.checkbox_r.setChecked(True)
                self.checkbox_g.setChecked(True)
                self.checkbox_b.setChecked(True)
                self.checkbox_swap.setChecked(False)



    def set_format(self, i):
        if i == 0:
            self.format = YUVFormat.YUYV_LE
        elif i == 1:
            self.format = YUVFormat.UYVY_LE
        elif i == 2:
            self.format = YUVFormat.YVYU_LE
        elif i == 3:
            self.format = YUVFormat.VYUY_LE

        elif i == 4:
            self.format = RGBFormat.BGR3_LE
        elif i == 5:
            self.format = RGBFormat.RGB3_LE
        elif i == 6:
            self.format = RGBFormat.XR24_LE
        elif i == 7:
            self.format = RGBFormat.RGBP_LE

        self.checkbox_state()
        self.match_format()


    def asign_format(self):
        pa = Parser._Parser(self.filepath, self.format, self.imgwidth, self.imgheight)
        self._format = self.format

        if self.format > 0 and self.format < 9:
            data = {'y':1, 'u':1, 'v':1}
            if (
                    self.format == YUVFormat.YUYV_LE or self.format == YUVFormat.UYVY_LE
                    or self.format == YUVFormat.YVYU_BE or self.format == YUVFormat.VYUY_BE
                ):
                if not self.checkbox_y.isChecked():
                    data['y'] = 0
                if not self.checkbox_u.isChecked():
                    data['u'] = 0
                if not self.checkbox_v.isChecked():
                    data['v'] = 0
            elif (
                    self.format == YUVFormat.YVYU_LE or self.format == YUVFormat.VYUY_LE
                    or self.format == YUVFormat.YUYV_BE or self.format == YUVFormat.UYVY_BE
                ):
                if not self.checkbox_y.isChecked():
                    data['y'] = 0
                if not self.checkbox_u.isChecked():
                    data['v'] = 0
                if not self.checkbox_v.isChecked():
                    data['u'] = 0
        elif self.format > 10 and self.format < 19:
            data = {'r':1, 'g':1, 'b':1}
            if (
                    self.format == RGBFormat.BGR3_LE or self.format == RGBFormat.RGB3_LE
                    or self.format == RGBFormat.XR24_BE or self.format == RGBFormat.RGBP_BE
                ):
                if not self.checkbox_r.isChecked():
                    data['b'] = 0
                if not self.checkbox_g.isChecked():
                    data['g'] = 0
                if not self.checkbox_b.isChecked():
                    data['r'] = 0
            elif (
                    self.format == RGBFormat.XR24_LE or self.format == RGBFormat.RGBP_LE
                    or self.format == RGBFormat.BGR3_BE or self.format == RGBFormat.RGB3_BE
                ):
                if not self.checkbox_r.isChecked():
                    data['r'] = 0
                if not self.checkbox_g.isChecked():
                    data['g'] = 0
                if not self.checkbox_b.isChecked():
                    data['b'] = 0

        _pixmap = pa.decode(data)
        self.pix = _pixmap
        self.label_img.setPixmap(self.pix)
        self.LineEdit_width.setText(str(self.imgwidth))
        self.LineEdit_height.setText(str(self.imgheight))

        log = LogObject(self)


    def swap_format(self):
        if self.radiobutton_le.isChecked():
            if self.checkbox_swap.isChecked() or not self.checkbox_swap.isChecked():
                if self.format == YUVFormat.YUYV_LE:
                    self.format = YUVFormat.YVYU_LE
                elif self.format == YUVFormat.UYVY_LE:
                    self.format = YUVFormat.VYUY_LE
                elif self.format == YUVFormat.YVYU_LE:
                    self.format = YUVFormat.YUYV_LE
                elif self.format == YUVFormat.VYUY_LE:
                    self.format = YUVFormat.UYVY_LE
        elif self.radiobutton_be.isChecked():
            if self.checkbox_swap.isChecked() or not self.checkbox_swap.isChecked():
                if self.format == YUVFormat.YUYV_BE:
                    self.format = YUVFormat.YVYU_BE
                elif self.format == YUVFormat.UYVY_BE:
                    self.format = YUVFormat.VYUY_BE
                elif self.format == YUVFormat.YVYU_BE:
                    self.format = YUVFormat.YUYV_BE
                elif self.format == YUVFormat.YVYU_BE:
                    self.format = YUVFormat.YUYV_BE

        self.asign_format()


    def match_format(self):
        if self.format > 0 and self.format < 9:
            if self.radiobutton_le.isChecked():
                if self.format == YUVFormat.VYUY_BE:
                    self.format = YUVFormat.YUYV_LE
                elif self.format == YUVFormat.YVYU_BE:
                    self.format = YUVFormat.UYVY_LE
                elif self.format == YUVFormat.UYVY_BE:
                    self.format = YUVFormat.YVYU_LE
                elif self.format == YUVFormat.YUYV_BE:
                    self.format = YUVFormat.VYUY_LE
            elif self.radiobutton_be.isChecked():
                if self.format == YUVFormat.YUYV_LE:
                    self.format = YUVFormat.VYUY_BE
                elif self.format == YUVFormat.UYVY_LE:
                    self.format = YUVFormat.YVYU_BE
                elif self.format == YUVFormat.YVYU_LE:
                    self.format = YUVFormat.UYVY_BE
                elif self.format == YUVFormat.VYUY_LE:
                    self.format = YUVFormat.YUYV_BE

        elif self.format > 10 and self.format < 19:
            if self.radiobutton_le.isChecked():
                if self.format == RGBFormat.RGBP_BE:
                    self.format = RGBFormat.BGR3_LE
                elif self.format == RGBFormat.XR24_BE:
                    self.format = RGBFormat.RGB3_LE
                elif self.format == RGBFormat.RGB3_BE:
                    self.format = RGBFormat.XR24_LE
                elif self.format == RGBFormat.BGR3_BE:
                    self.format = RGBFormat.RGBP_LE
            elif self.radiobutton_be.isChecked():
                if self.format == RGBFormat.BGR3_LE:
                    self.format = RGBFormat.RGBP_BE
                elif self.format == RGBFormat.RGB3_LE:
                    self.format = RGBFormat.XR24_BE
                elif self.format == RGBFormat.XR24_LE:
                    self.format = RGBFormat.RGB3_BE
                elif self.format == RGBFormat.RGBP_LE:
                    self.format = RGBFormat.BGR3_BE

        self.asign_format()


    def load_to_sub(self, picture):
        MainWindow.count = MainWindow.count+1

        sub = QMdiSubWindow(self)
        loaded_picture = LoadPicture(picture, sub)

        sub.setWidget(loaded_picture)
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo"+str(MainWindow.count))
        self.mdiArea.addSubWindow(sub)

        sub.show()
        sub.resize(500, 500)
        loaded_picture.log.MousePixmapSignal.connect(self.update_pixel)


    def update_pixel(self, point, color):
        self.UserInput_PixelValue_X.setText("{}".format(point.x()))
        self.UserInput_PixelValue_Y.setText("{}".format(point.y()))

        self.UserInput_PixelValue_R.setText("{}".format(color.red()))
        self.UserInput_PixelValue_G.setText("{}".format(color.green()))
        self.UserInput_PixelValue_B.setText("{}".format(color.blue()))


    def auto_detect(self):
        try:
            if self.format > 0 and self.format < 19:
                data = {'y':1, 'u':1, 'v':1}
                for i in range(4):
                    if 0 < self.format < 5:
                        self.format = i + 1
                    else:
                        self.format = i + 5
                    pa = Parser._Parser(self.filepath, self.format, self.imgwidth, self.imgheight)
                    if self.format == 1 or self.format == 2:
                        if not self.checkbox_y.isChecked():
                            data['y'] = 0
                        if not self.checkbox_u.isChecked():
                            data['u'] = 0
                        if not self.checkbox_v.isChecked():
                            data['v'] = 0
                    else:
                        if not self.checkbox_y.isChecked():
                            data['y'] = 0
                        if not self.checkbox_u.isChecked():
                            data['v'] = 0
                        if not self.checkbox_v.isChecked():
                            data['u'] = 0
                    _pixmap = pa.decode(data)
                    self.pix = _pixmap
                    self.load_to_sub(self.pix)

            elif self.format > 10 and self.format < 19:
                data = {'r':1, 'g':1, 'b':1}
                for i in range(4):
                    if 10 < self.format < 15:
                        self.format = i + 11
                    else:
                        self.format = i + 15
                    pa = Parser._Parser(self.filepath, self.format, self.imgwidth, self.imgheight)
                    if self.format == 11 or self.format == 12:
                        if not self.checkbox_r.isChecked():
                            data['r'] = 0
                        if not self.checkbox_g.isChecked():
                            data['g'] = 0
                        if not self.checkbox_b.isChecked():
                            data['b'] = 0
                    else:
                        if not self.checkbox_r.isChecked():
                            data['r'] = 0
                        if not self.checkbox_g.isChecked():
                            data['b'] = 0
                        if not self.checkbox_b.isChecked():
                            data['g'] = 0
                    _pixmap = pa.decode(data)
                    self.pix = _pixmap
                    self.load_to_sub(self.pix)
        except TypeError:
            pass                


    def update_size(self):
        if self.LineEdit_width.text():
            self.imgwidth = int(self.LineEdit_width.text())

    def update_size2(self):
        if self.LineEdit_height.text():
            self.imgheight = int(self.LineEdit_height.text())


    def zoom_in(self):
        try:
            self.factor += 0.05
            _width = self.imgwidth
            _height = self.imgheight
            _width = int(self.imgwidth * self.factor)
            _height = int(self.imgheight * self.factor)
            self.label_img.setPixmap(self.pix.scaled(_width, _height, Qt.KeepAspectRatio))
            self.LineEdit_width.setText(str(_width))
            self.LineEdit_height.setText(str(_height))
        except AttributeError:
            pass


    def zoom_out(self):
        try:
            self.factor -= 0.05
            _width = self.imgwidth
            _height = self.imgheight
            _width = int(self.imgwidth * self.factor)
            _height = int(self.imgheight * self.factor)
            self.label_img.setPixmap(self.pix.scaled(_width, _height, Qt.KeepAspectRatio))
            self.LineEdit_width.setText(str(_width))
            self.LineEdit_height.setText(str(_height))
        except AttributeError:
            pass




if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = MainWindow()
    WINDOW.setWindowTitle('Raw Image viewer')
    WINDOW.show()
    sys.exit(APP.exec_())

"""
        while True:
            try:
                self.factor += 0.05
                _width = self.imgwidth
                _height = self.imgheight
                _width = int(self.imgwidth * self.factor)
                _height = int(self.imgheight * self.factor)
                self.label_img.setPixmap(self.pix.scaled(_width, _height, Qt.KeepAspectRatio))
                self.LineEdit_width.setText(str(_width))
                self.LineEdit_height.setText(str(_height))
                break
            except AttributeError:
                ans = QMessageBox.Warning(self, "error", "You should open the file first.") #QMessageBox.Yes)
                if ans == QMessageBox.Yes:
                    pass
"""