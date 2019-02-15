#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disble = missing-docstring
#pylint:disable = no-name-in-module

#pip install numexpr==2.6.1

import sys
from enum import Enum, IntEnum
import array
import inspect

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QFile


from main import *
from LoadPicture import *
from PIL import Image
import cv2
import numpy as np
import array

#Ian's zero pending...bb
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


class _Parser:
    __DECODE_MAP = {
        #color:[bit per pixel, desc]
        'YUV422':[16, "YUV 4:2:2"],
        'RGB3':[24, "green 8bits, red 8bits, blue 8bits"],
        'XR24':[32, "green 8bits, red 8bits, blue 8bits, alpha 8bits"],
        'RGBP':[16, "green 6bits, red 5bits, blue 5bits"]
        }


    def getbpp(cls, color):
        return cls.__DECODE_MAP[color][0]

#variable name
#_variablename means protected things
#So, if i want to use that, __variable /or/ another name
    def __init__(self, _filepath, _format, _imgwidth, _imgheight):
        self._filepath_ = _filepath #__를 앞
        self._format_ = _format
        self._imgwidth_ = _imgwidth
        self._imgheight_ = _imgheight
        self._data_ = {}
        self._filesize_ = None
        self._bufsize_ = None
        self._bpp_ = None


    def decode(self, choice):
        try:
            width = self._imgwidth_
            height = self._imgheight_
            form = self._format_
            filepath = self._filepath_
            self._data_.update(choice)

            f_val = open(filepath, "rb")

            #will open the file for read mode (r) with binary I/O (b).

            file = QFile(filepath)
            self._filesize_ = file.size()  #f_size = w*h*bpp/3


            if YUVFormat.YUYV_LE <= form <= YUVFormat.VYUY_BE:
                image_out = self.YUV422(width, height, form, f_val)

            elif form == RGBFormat.RGB3_LE or form == RGBFormat.RGB3_BE:
                image_out = self.RGB3(width, height, form, f_val)

            elif form == RGBFormat.BGR3_LE or form == RGBFormat.BGR3_BE:
                image_out = self.BGB3(width, height, form, f_val)

            elif form == RGBFormat.XR24_LE or form == RGBFormat.XR24_BE:
                image_out = self.XRGB(width, height, f_val)

            elif form == RGBFormat.RGBP_LE or form == RGBFormat.RGBP_BE:
                image_out = self.RGBP(width, height, f_val)

            data = image_out.tobytes('raw', "RGB")
            qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qim)
            return pixmap

        except FileNotFoundError:
            pass


    def YUV422(self, width, height, form, f_uyvy):
        #Each four bytes is two pixels.
        #Each four bytes is two Y’s, a Cb and a Cr.
        #Y goes to one of the pixels,
        #and the Cb and Cr belong to both pixels. As you can see,
        #the Cr and Cb components have half the horizontal resolution of the Y component.

        self._bpp_ = self.getbpp('YUV422')
        self._bufsize_ = width * height * (self._bpp_ / 8)

        # Read entire file into YUV
        im = np.fromfile(f_uyvy, dtype=np.uint8)
        #width = 1920
        #height = 1080
        #wh = width * height
        width = self._imgwidth_
        height = self._imgheight_
        wh = int(self._filesize_ / (self._bpp_ / 8))

        if form == YUVFormat.YUYV_LE or form == YUVFormat.YUYV_BE:
            try:
                Y1  = im[0::4]
                U = im[1::4]
                Y2  = im[2::4]
                V = im[3::4]
            except:
                pass

        elif form == YUVFormat.UYVY_LE or form == YUVFormat.UYVY_BE:
            try:
                U  = im[0::4]
                Y1 = im[1::4]
                V  = im[2::4]
                Y2 = im[3::4]
            except:
                pass

        elif form == YUVFormat.YVYU_LE or form == YUVFormat.YVYU_BE:
            try:
                Y1  = im[0::4]
                V = im[1::4]
                Y2  = im[2::4]
                U = im[3::4]
            except:
                pass

        elif form == YUVFormat.VYUY_LE or form == YUVFormat.VYUY_BE:
            try:
                V  = im[0::4]
                Y1 = im[1::4]
                U  = im[2::4]
                Y2 = im[3::4]
            except:
                pass

        #ValueError: ndarray is not C-contiguous
        U = U.copy(order='C')
        Y1 = Y1.copy(order='C')
        V = V.copy(order='C')
        Y2 = Y2.copy(order='C')

        UV = np.zeros(wh, dtype=np.uint8)
        YY = np.zeros(wh, dtype=np.uint8)

        if self._data_ != {'y':1, 'u':1, 'v':1}:
            Y1, Y2, U, V = self.choice_yuvval(Y1, Y2, U, V)

        if(
                form == YUVFormat.UYVY_LE or form == YUVFormat.UYVY_BE
                or form == YUVFormat.YUYV_LE or form == YUVFormat.YUYV_BE
        ):
            UV[0::2] = np.fromstring(V, dtype=np.uint8)
            UV[1::2] = np.fromstring(U, dtype=np.uint8)
        elif(
                form == YUVFormat.VYUY_LE or form == YUVFormat.VYUY_BE
                or form == YUVFormat.YVYU_LE or form == YUVFormat.YVYU_BE
        ):
            UV[0::2] = np.fromstring(V, dtype=np.uint8)
            UV[1::2] = np.fromstring(U, dtype=np.uint8)

        YY[0::2] = np.fromstring(Y1, dtype=np.uint8)
        YY[1::2] = np.fromstring(Y2, dtype=np.uint8)

        #UV = UV.reshape(height, width)
        #YY = YY.reshape(height, width)

        yuv422 = cv2.merge([UV, YY])

        bgr  = cv2.cvtColor(yuv422, cv2.COLOR_YUV2BGR_UYVY)

        #Creates an image memory referencing pixel data in a byte buffer.
        image_out = Image.frombuffer("RGB",[width, height], bgr, 'raw', 'RGB', 0, 1)

        return image_out


    def choice_yuvval(self, y1, y2, u, v):
        if self._data_['y'] == 0:
            y1[:] = 0
            y2[:] = 0
        if self._data_['u'] == 0:
            u[:] = 0
        if self._data_['v'] == 0:
            v[:] = 0
        return (y1, y2, u, v)


    def RGB3(self, width, height, form, f_rgb):
        self._bpp_ = self.getbpp('RGB3')
        self._bufsize_ = width * height * (self._bpp_ / 8)
        wh = int(self._filesize_ / (self._bpp_ / 8))

        im = np.fromfile(f_rgb, dtype=np.uint8)
        #buf = np.zeros(wh, 3), dtype=np.uint8)

        im = im.reshape(-1, 3)
        #im = im.reshape(width, height, 3)
        #data = np.asarray(im)

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            a = self.choice_val(im)
            im = a

        image_out = Image.frombuffer("RGB",[width, height], im, 'raw','BGR', 0, 1)

        return image_out


    def BGB3(self, width, height, form, f_rgb):
        self._bpp_ = self.getbpp('RGB3')
        self._bufsize_ = width * height * (self._bpp_ / 8)
        wh = int(self._filesize_ / (self._bpp_ / 8))

        im = np.fromfile(f_rgb, dtype=np.uint8)
        #buf = np.zeros(wh, 3), dtype=np.uint8)

        im = im.reshape(-1, 3)
        #im = im.reshape(width, height, 3)
        #data = np.asarray(im)

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            a = self.choice_val(im)
            im = a

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            if self._data_['b'] == 0:
                im = np.delete(im, 0, 1)
                im = np.insert(im, 0, 0, 1)
            if self._data_['g'] == 0:
                im = np.delete(im, 1, 1)
                im = np.insert(im, 1, 0, 1)
            if self._data_['r'] == 0:
                im = np.delete(im, 2, 1)
                im = np.insert(im, 2, 0, 1)

        image_out = Image.frombuffer("RGB",[width, height], im, 'raw','RGB', 0, 1)

        return image_out


    def XRGB(self, width, height, f_rgb):
        self._bpp_ = self.getbpp('XR24')
        self._bufsize_ = width * height * (self._bpp_ / 8)

        im = np.fromfile(f_rgb, dtype=np.uint8)
        im = im.reshape(-1, 4)
        im = np.delete(im, 3, 1)
        im = im.reshape(-1, 3)

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            a = self.choice_val(im)
            im = a

        image_out = Image.frombuffer("RGB",[width, height], im, 'raw','RGB', 0, 1)

        return image_out



    def RGBP(self, width, height, f_rgb):
        self._bpp_ = self.getbpp('RGBP')
        self._bufsize_ = width * height * (self._bpp_ / 8)

        #RRRR RGGG GGGB BBBB
        im = np.fromfile(f_rgb, dtype=np.uint16).astype(np.uint32)

        #alpha = 0xff
        red = ((im & 0xF800) >> 8) # (arr & 0xf800) >> 11; b << 3;
        green = ((im & 0x07E0) << 5) # (arr & 0x07e0) >> 5; g  = g << 2; g << 8
        blue = ((im & 0x001F) << 19) # (arr & 0x001f); r << 3; r << 16

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            if self._data_['r'] == 0:
                red = 0
            if self._data_['g'] == 0:
                green = 0
            if self._data_['b'] == 0:
                blue = 0

        im = 0xFF000000 + blue + green + red

        image_out = Image.frombuffer("RGBA",[width, height], im, 'raw','RGBA', 0, 1)

        return image_out


    def choice_val(self, im):
        if self._data_['r'] == 0:
            im = np.delete(im, 0, 1)
            im = np.insert(im, 0, 0, 1)
        if self._data_['g'] == 0:
            im = np.delete(im, 1, 1)
            im = np.insert(im, 1, 0, 1)
        if self._data_['b'] == 0:
            im = np.delete(im, 2, 1)
            im = np.insert(im, 2, 0, 1)
        return im


    def send(self):
        return self._filesize_, self._bufsize_, self._bpp_
