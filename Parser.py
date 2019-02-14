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
#import cv2
#import numpy as np
#import numexpr as ne
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

    def getsize(self):
        print('File size(bytes):', int(self._filesize_))
        print('Want to read file size(bytes):', int(self._bufsize_))
        print('byte:', int(self._bpp_ / 8))
        print('File w*h:', int(self._filesize_ / (self._bpp_ / 8)))
        print('Want to read file w*h:', int(self._bufsize_ / (self._bpp_ / 8)))

#using Dictonary
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
                self._bpp_ = self.getbpp('YUV422')
                self._bufsize_ = width * height * (self._bpp_ / 8)
                image_out = self.YUV422(width, height, form, f_val)

            elif (
                    form == RGBFormat.BGR3_LE or form == RGBFormat.BGR3_BE
                    or form == RGBFormat.RGB3_LE or form == RGBFormat.RGB3_BE
            ):
                self._bpp_ = self.getbpp('RGB3')
                self._bufsize_ = width * height * (self._bpp_ / 8)
                image_out = self.RGB3(width, height, form, f_val)

            elif form == RGBFormat.XR24_LE or form == RGBFormat.XR24_BE:
                self._bpp_ = self.getbpp('XR24')
                self._bufsize_ = width * height * (self._bpp_ / 8)
                image_out = self.XRGB(width, height, f_val)

            elif form == RGBFormat.RGBP_LE or form == RGBFormat.RGBP_BE:
                self._bpp_ = self.getbpp('RGBP')
                self._bufsize_ = width * height * (self._bpp_ / 8)
                image_out = self.RGBP(width, height, f_val)

            data = image_out.tobytes('raw', "RGB")
            qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qim)
            return pixmap
        except FileNotFoundError:
            pass


    def YUV422(self, width, height, form, f_uyvy):
        self.getsize()

        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()


        for i in range(0, height):
            for j in range(0, int(width/2)):
                pix_y1 = pix_u = pix_y2 = pix_v = 0

                if form == YUVFormat.YUYV_LE or form == YUVFormat.YUYV_BE:
                    try:
                        pix_y1, pix_u, pix_y2, pix_v = (b for b in f_uyvy.read(4))
                    except:
                        pass

                elif form == YUVFormat.UYVY_LE or form == YUVFormat.UYVY_BE:
                    try:
                        pix_u, pix_y1, pix_v, pix_y2 = (b for b in f_uyvy.read(4))
                    except:
                        pass

                elif form == YUVFormat.YVYU_LE or form == YUVFormat.YVYU_BE:
                    try:
                        pix_y1, pix_v, pix_y2, pix_u = (b for b in f_uyvy.read(4))
                    except:
                        pass

                elif form == YUVFormat.VYUY_LE or form == YUVFormat.VYUY_BE:
                    try:
                        pix_v, pix_y1, pix_u, pix_y2 = (b for b in f_uyvy.read(4))
                    except:
                        pass

                (
                    pix_y1, pix_y2, pix_u, pix_v
                ) = self.choice_yuvval(
                    pix_y1, pix_y2, pix_u, pix_v
                )


                red = 1.164 * (pix_y1-16) + 2.018 * (pix_u - 128)
                green = 1.164 * (pix_y1-16) - 0.813 * (pix_v - 128) - 0.391 * (pix_u - 128)
                blue = 1.164 * (pix_y1-16) + 1.596 * (pix_v - 128)
                pix[j*2, i] = int(blue), int(green), int(red)

                red = 1.164 * (pix_y2-16) + 2.018 * (pix_u - 128)
                green = 1.164 * (pix_y2-16) - 0.813 * (pix_v - 128) - 0.391 * (pix_u - 128)
                blue = 1.164 * (pix_y2-16) + 1.596 * (pix_v - 128)
                pix[j*2+1, i] = int(blue), int(green), int(red)


        return image_out


    def choice_yuvval(self, _y1, _y2, _u, _v):
        if self._data_['y'] == 0:
            _y1 = 16
            _y2 = 16
        if self._data_['u'] == 0:
            _u = 128
        if self._data_['v'] == 0:
            _v = 128
        return (_y1, _y2, _u, _v)



    def RGB3(self, width, height, form, f_rgb):
        self.getsize()
        sel = 0
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = pix_g = pix_b = 0
                if form == RGBFormat.BGR3_LE or form == RGBFormat.BGR3_BE:
                    try:
                        pix_r, pix_g, pix_b = (b for b in f_rgb.read(3))
                    except:
                        pass

                elif form == RGBFormat.RGB3_LE or form == RGBFormat.RGB3_BE:
                    try:
                        pix_b, pix_g, pix_r = (b for b in f_rgb.read(3))
                    except:
                        pass

                if sel == 1:
                    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = int(pix_b), int(pix_g), int(pix_r)

        return image_out


    def XRGB(self, width, height, f_rgb):
        self.getsize()
        sel = 0
        ##1. array
        #im = array.array('B')
        #im.frombytes(f_rgb.read())
        ##2. numpy
        im = f_rgb.read()

        image_out = Image.new("RGB", (width, height), (0,0,0))
        #image_out = np.zeros((width, height, 4), dtype=np.uint8)
        pix = image_out.load()

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = pix_g = pix_b = pix_a = 0
                try:
                    #pix_r, pix_g, pix_b, pix_a = (b for b in f_rgb.read(4))
                    pix_r = im[(width*i+j)*4]
                    pix_g = im[(width*i+j)*4+1]
                    pix_b = im[(width*i+j)*4+2]

                except:
                    pass

                if sel == 1:
                    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = pix_r, pix_g, pix_b

        return image_out




    def RGBP(self, width, height, f_rgb):
        self.getsize()
        sel = 0
        #im = array.array('B')
        #im.frombytes(f_rgb.read())
        im = f_rgb.read()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()


        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_h = pix_l = 0
                try:
                    #pix_h, pix_l = (b for b in f_rgb.read(2))
                    pix_h = im[(width*i+j)*4]
                    pix_l = im[(width*i+j)*4+1]
                except:
                    pass

                value = pix_l*256 + pix_h

                blue = (value & 0xF800) >> 8
                green = (value & 0x7E0) >> 3
                red = (value & 0x1F) << 3

                if sel == 1:
                    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = int(red), int(green), int(blue)


        return image_out


    def choice_rgbval(self, pix_b, pix_g, pix_r):
        if self._data_['b'] == 0:
            pix_b = 0
        if self._data_['g'] == 0:
            pix_g = 0
        if self._data_['r'] == 0:
            pix_r = 0

        return (pix_b, pix_g, pix_r)

"""
    def XRGB(self, width, height, f_rgb):
        self.getsize()
        #sel = 0
        #im = cv2.imread(self._filepath_)

        ##1. array
        #im = array.array('B')
        #im.frombytes(f_rgb.read())
        ##2. numpy
        im = f_rgb.read()

        #im = np.zeros([width, height, 4], dtype=np.uint8)
        #im = np.fromstring(f_rgb.tobytes(),np.uint8)

        #im.asarray(img, dtype="int32")

        #im = np.asarray(f_rgb, dtype="int32" )

        #img = np.array(f_rgb)
        #im = np.asarray(img, dtype="int32")
        #array = np.zeros([width, height, 4], dtype=np.uint8)
        #array[:,:100] = [255, 128, 0, 255] #Orange left side
        #array[:,100:] = [0, 0, 255, 255] #Blue right side

        #im = np.fromstring(f_rgb.tobytes(),np.uint8)
        #im = im.reshape((f_rgb.size[1], f_rgb.size[0], 4))

        image_out = Image.new("RGB", (width, height), (0,0,0))
        #image_out = np.zeros((width, height, 4), dtype=np.uint8)
        pix = image_out.load()



        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = pix_g = pix_b = pix_a = 0
                try:
                    #pix_r, pix_g, pix_b, pix_a = (b for b in f_rgb.read(4))
                    pix_r = im[(width*i+j)*4]
                    pix_g = im[(width*i+j)*4+1]
                    pix_b = im[(width*i+j)*4+2]
                    #print (pix_r)
                    #print (pix_g)
                    #print (pix_b)
                except:
                    pass

                #if sel == 1:
                #    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = pix_r, pix_g, pix_b

        return image_out

        #f_rgb = np.array(f_rgb)

"""
"""

        im = array.array('B')
        im.frombytes(f_rgb.read())

        image_out = Image.new("RGB", (width, height), (0,0,0))

        pix = image_out.load()
"""

"""
    def XRGB(self, width, height, f_rgb):
        self.getsize()
        sel = 0

        #im = cv2.imread(self._filepath_)
        im = np.fromstring(f_rgb.tobytes(),np.uint8)
        im = im.reshape((f_rgb.size[1], f_rgb.size[0], 4))

        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()
        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = pix_g = pix_b = pix_a = 0
                try:
                    pix_r, pix_g, pix_b, pix_a = (b for b in f_rgb.read(4))

                except:
                    pass

                if sel == 1:
                    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = pix_r, pix_g, pix_b

        return image_out

        #f_rgb = np.array(f_rgb)

"""

"""

    def XRGB(self, width, height, f_rgb):
        self.getsize()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()
        sel = 0

        if self._data_ != {'r':1, 'g':1, 'b':1}:
            sel = 1

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = pix_g = pix_b = pix_a = 0
                try:
                    pix_r, pix_g, pix_b, pix_a = (b for b in f_rgb.read(4))
                except:
                    pass

                if sel == 1:
                    (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix[j, i] = pix_r, pix_g, pix_b

        return image_out

        #f_rgb = np.array(f_rgb)

"""


"""

        Total_wh = int(self._filesize_ / (self._bpp_ / 8))
        Want_wh = int(self._bufsize_ / (self._bpp_ / 8))

"""

"""
        for i in range(0, height):
            for j in range(0, int(width/2)):
                if form == YUVFormat.YUYV_LE or form == YUVFormat.YUYV_BE:
                    pix_y1 = ord(f_uyvy.read(1))
                    pix_u = ord(f_uyvy.read(1))
                    pix_y2 = ord(f_uyvy.read(1))
                    pix_v = ord(f_uyvy.read(1))
                elif form == YUVFormat.UYVY_LE or form == YUVFormat.UYVY_BE:
                    pix_u = ord(f_uyvy.read(1))
                    pix_y1 = ord(f_uyvy.read(1))
                    pix_v = ord(f_uyvy.read(1))
                    pix_y2 = ord(f_uyvy.read(1))
                elif form == YUVFormat.YVYU_LE or form == YUVFormat.YVYU_BE:
                    pix_y1 = ord(f_uyvy.read(1))
                    pix_v = ord(f_uyvy.read(1))
                    pix_y2 = ord(f_uyvy.read(1))
                    pix_u = ord(f_uyvy.read(1))
                elif form == YUVFormat.VYUY_LE or form == YUVFormat.VYUY_BE:
                    pix_v = ord(f_uyvy.read(1))
                    pix_y1 = ord(f_uyvy.read(1))
                    pix_u = ord(f_uyvy.read(1))
                    pix_y2 = ord(f_uyvy.read(1))
"""
"""
            f_val = open(filepath, "rb")

            file = QFile(filepath)
            self._filesize_ = file.size()  #f_size = w*h*bpp/3

"""
