#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disble = missing-docstring
#pylint:disable = no-name-in-module

import sys
from enum import Enum, IntEnum
import array
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QFile
from main import *
from LoadPicture import *
from PIL import Image
import inspect



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


    def __init__(self, _filepath, _format, _imgwidth, _imgheight):
        self._filepath_ = _filepath
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
        #except FileNotFoundError:
        #    pass
        #except TypeError:
        #    pass



    def YUV422(self, width, height, form, f_uyvy):
        self.getsize()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()

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
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()

        for i in range(0, height):
            for j in range(0, int(width)):
                if form == RGBFormat.BGR3_LE or form == RGBFormat.BGR3_BE:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))

                elif form == RGBFormat.RGB3_LE or form == RGBFormat.RGB3_BE:
                    pix_b = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_r = ord(f_rgb.read(1))


                (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                red = pix_r
                green = pix_g
                blue = pix_b

                pix[j, i] = int(blue), int(green), int(red)

        return image_out

    def getsize(self):
        print('File size(bytes):', int(self._filesize_))
        print('Want to read file size(bytes):', int(self._bufsize_))
        print('byte:', int(self._bpp_ / 8))
        print('File w*h:', int(self._filesize_ / (self._bpp_ / 8)))
        print('Want to read file w*h:', int(self._bufsize_ / (self._bpp_ / 8)))


    def XRGB(self, width, height, f_rgb):
        self.getsize()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()
        Total_wh = int(self._filesize_ / (self._bpp_ / 8))
        Want_wh = int(self._bufsize_ / (self._bpp_ / 8))

        for i in range(0, height):
            for j in range(0, int(width)):
                try:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))
                    break
                except Total_wh - Want_wh < 0:
                    pass

                (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix_a = 0
                blue = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                red = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255

                pix[j, i] = int(blue), int(green), int(red)

        return image_out



    def RGBP(self, width, height, f_rgb):
        self.getsize()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_h = ord(f_rgb.read(1))
                pix_l = ord(f_rgb.read(1))

                value = pix_l*256 + pix_h

                blue = (value & 0xF800) >> 8
                green = (value & 0x7E0) >> 3
                red = (value & 0x1F) << 3

                (blue, green, red) = self.choice_rgbval(blue, green, red)

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
        for i in range(0, height):
            for j in range(0, int(width)):
                try:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))
                    break
                except Total_wh - Want_wh < 0:
                    pass

"""

"""
    def XRGB(self, width, height, f_rgb):
        self.getsize()
        image_out = Image.new("RGB", (width, height), (0,0,0))
        pix = image_out.load()

        for i in range(0, height):
            for j in range(0, int(width)):
                pix_r = ord(f_rgb.read(1))
                pix_g = ord(f_rgb.read(1))
                pix_b = ord(f_rgb.read(1))
                pix_a = ord(f_rgb.read(1))

                (pix_b, pix_g, pix_r) = self.choice_rgbval(pix_b, pix_g, pix_r)

                pix_a = 0
                blue = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                red = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255

                pix[j, i] = int(blue), int(green), int(red)

        return image_out

"""
