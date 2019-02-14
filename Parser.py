#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disble=missing-docstring
#pylint:disable=no-name-in-module

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main import *
from LoadPicture import *

from enum import Enum, IntEnum
import numpy as np
import array
from PIL import Image



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
    def __init__(self, _filepath, _format, _imgwidth, _imgheight):
        self._filepath_ = _filepath
        self._format_ = _format
        self._imgwidth_ = _imgwidth
        self._imgheight_ = _imgheight
        self._data_ = {}


    def decode_yuv(self, choice):
        """doc string"""
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_
        f_uyvy = open(img_name, "rb")

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()
        self._data_.update(choice)

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


                pix_y1 = 1.164 * (pix_y1-16)
                pix_u_b = 2.018 * (pix_u - 128)
                pix_u_g = - 0.391 * (pix_u - 128)
                pix_y2 = 1.164 * (pix_y2-16)
                pix_v_g = - 0.813 * (pix_v - 128)
                pix_v_r = 1.596 * (pix_v - 128)


                if self._data_['y'] == 0:
                    pix_y1 = 0
                    pix_y2 = 0
                if self._data_['u'] == 0:
                    pix_u_b = 0
                    pix_u_g = 0
                if self._data_['v'] == 0:
                    pix_v_g = 0
                    pix_v_r = 0

                blue = pix_y1 + pix_u_b
                green = pix_y1 + pix_v_g + pix_u_g
                red = pix_y1 + pix_v_r
                pix[j*2, i] = int(red), int(green), int(blue)

                blue = pix_y2 + pix_u_b
                green = pix_y2 + pix_v_g + pix_u_g
                red = pix_y2 + pix_v_r
                pix[j*2+1, i] = int(red), int(green), int(blue)


        data = image_out.tobytes('raw', "RGB")
        qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

#############
    def decode_rgb(self, choice):
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_
        f_rgb = open(img_name, "rb")

        image_out = Image.new("RGBA", (width, height))
        pix = image_out.load()
        self._data_.update(choice)


        for i in range(0, height):
            for j in range(0, int(width)):
                if form == RGBFormat.XR24_LE or form == RGBFormat.XR24_BE:
                    pix_b = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_r = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))


                    if self._data_['b'] == 0:
                        pix_r = 0
                    if self._data_['g'] == 0:
                        pix_g = 0
                    if self._data_['r'] == 0:
                        pix_b = 0


                    pix_a = 0
                    red = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                    green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                    blue = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255

                    pix[j,i] = int(blue), int(green), int(red)


        data = image_out.tobytes('raw', "RGB")
        qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap



"""
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

"""


"""


                red = ((1 - pix_a) * pix_r) + (pix_a * pix_r)
                green = ((1 - pix_a) * pix_g) + (pix_a * pix_g)
                blue = ((1 - pix_a) * pix_b) + (pix_a * pix_b)
                alpha = 1

"""




"""
    def blend_value(self, under, over, a):
        return int((over*a + under*(255-a)) / 255)

    def blend_rgba(self, under, over):
        return tuple([self.blend_value(under[i], over[i], over[3]) for i in (0,1,2)] + [255])



    def decode_rgb(self, choice):
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_

        f_rgb = open(img_name, "rb")
        image_out = Image.new("RGBA", (width, height))
        pix = image_out.load()
        for y in range(0, height):
            for x in range(0, width):
                pix_b = ord(f_rgb.read(1))
                pix_g = ord(f_rgb.read(1))
                pix_r = ord(f_rgb.read(1))
                pix_a = ord(f_rgb.read(1))

                alpha = 0
                red = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                blue = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255

                pix[x,y] = int(blue) + int(green) + int(red) + int(alpha)
                #pix[x,y] = int(blue) + 0 + 0 + 0


        data = image_out.tobytes('raw', "RGB")
        qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap
"""

"""
"""

"""

"""
"""
                red = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                blue = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255


"""
"""
arget.R = ((1 - Source.A) * BGColor.R) + (Source.A * Source.R)
Target.G = ((1 - Source.A) * BGColor.G) + (Source.A * Source.G)
Target.B = ((1 - Source.A) * BGColor.B) + (Source.A * Source.B)

  $ored: ((1 - alpha($fore)) * red($back) ) + (alpha($fore) * red($fore));
    $ogreen: ((1 - alpha($fore)) * green($back) ) + (alpha($fore) * green($fore));
      $oblue: ((1 - alpha($fore)) * blue($back) ) + (alpha($fore) * blue($fore));

    float red = (1 - alpha) * rgb_background_red + alpha * rgba_color_red;
        float green = (1 - alpha) * rgb_background_green + alpha * rgba_color_green;
            float blue = (1 - alpha) * rgb_background_blue + alpha * rgba_color_blue;
"""


"""

        for y in range(0, height):
            for x in range(0, width):
                pix_b = ord(f_rgb.read(1))
                pix_g = ord(f_rgb.read(1))
                pix_r = ord(f_rgb.read(1))
                pix_a = ord(f_rgb.read(1))


                pix_a = 0
                red = (pix_a * (pix_r / 255) + ((1 - pix_a) * (pix_r / 255))) * 255
                green = (pix_a * (pix_g / 255) + ((1 - pix_a) * (pix_g / 255))) * 255
                blue = (pix_a * (pix_b / 255) + ((1 - pix_a) * (pix_b / 255))) * 255

                pix[x,y] = int(blue) + int(green) + int(red)



"""

"""

        f_rgb = open(img_name, "rb")
        image_out2 = Image.new("RGBA", (width, height))
        x = np.array(image_out2)

        r, g, b, a = np.rollaxis(x, axis = -1)
        r[a == 0] = 255
        g[a == 0] = 255
        b[a == 0] = 255
        x = np.dstack([r, g, b, a])

        image_out = Image.fromarray(x, 'RGBA')


        f_rgb = open(img_name, "rb")
        image_out = Image.new("RGBA", (width, height))
        pix = image_out.load()




"""

"""
#see black image
    def blend_value(self, under, over, a):
        return int((over*a + under*(255-a)) / 255)

    def blend_rgba(self, under, over):
        return tuple([self.blend_value(under[i], over[i], over[3]) for i in (0,1,2)] + [255])



    def decode_rgb(self, choice):
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_

        f_rgb = open(img_name, "rb")
        image_out = Image.new("RGBA", (width, height))
        pix = image_out.load()
        white = (0, 0, 0, 0)


        for y in range(0, height):
            for x in range(0, width):
                pix[x,y] = self.blend_rgba(white, pix[x,y])


        data = image_out.tobytes('raw', "RGB")
        qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

"""


"""
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_
        f_uyvy = open(img_name, "rb")

        image_out = Image.new("RGB", (width, height))
        pix = image_out.load()
        self._data_.update(choice)

"""

"""
###########
    def alpha_composite(self,src, dst):
        src = np.asarray(src)
        dst = np.asarray(dst)
        out = np.empty(src.shape, dtype = 'float')
        alpha = np.index_exp[:, :, 3:]
        rgb = np.index_exp[:, :, :3]
        src_a = src[alpha]/255.0
        dst_a = dst[alpha]/255.0
        out[alpha] = src_a+dst_a*(1-src_a)
        old_setting = np.seterr(invalid = 'ignore')
        out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
        np.seterr(**old_setting)
        out[alpha] *= 255
        np.clip(out,0,255)
        # astype('uint8') maps np.nan (and np.inf) to 0
        out = out.astype('uint8')
        out = Image.fromarray(out, 'RGBA')
        return out

    def decode_rgb(self, choice):
        width = self._imgwidth_
        height = self._imgheight_
        form = self._format_

        img_name = self._filepath_


       # with Image.open(img_name) as f:
       #     a = f.convert('RGBA')
       #     b = io.BytesIO(a.read())

        f_rgb = open(img_name, "rb")
        #convert('RGBA')
        #f_uyvy = open(img_name, "rb")
        image_out = Image.new('RGBA', (width, height), color = (255, 255, 255, 255))
        im = self.alpha_composite(f_rgb, image_out)

        data = im.tobytes('raw', "RGB")
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap
"""

#        image_out = Image.new("RGB", (width, height))
#        pix = image_out.load()
#        self._data_.update(choice)

#        data = image_out.tobytes('raw', "RGB")
#        qim = QImage(data, image_out.size[0], image_out.size[1], QImage.Format_RGB888)
#        pixmap = QPixmap.fromImage(qim)
#        return pixmap




#FNAME = 'logo.png'
#img = Image.open(FNAME).convert('RGBA')

#white = Image.new('RGBA', size = img.size, color = (255, 255, 255, 255))
#img = alpha_composite(img, white)
#img.save('/tmp/out.jpg')





"""
        pix_r = array.array("B")
        pix_g = array.array("B")
        pix_b = array.array("B")
"""



"""
        for i in range(0, height):
            for j in range(0, int(width)):
               if form == RGBFormat.BGR3_LE.value or form == RGBFormat.BGR3_BE.value:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))
                elif form == RGBFormat.RGB3_LE.value or form == RGBFormat.RGB3_BE.value:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))
                elif form == RGBFormat.YXR24_LE.value or form == RGBFormat.XR24_BE.value:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))
                elif form == RGBFormat.RGBP_LE.value or form == RGBFormat.RGBP_BE.value:
                    pix_r = ord(f_rgb.read(1))
                    pix_g = ord(f_rgb.read(1))
                    pix_b = ord(f_rgb.read(1))
                    pix_a = ord(f_rgb.read(1))

                pix_y1 = 1.164 * (pix_y1-16)
                pix_u_b = 2.018 * (pix_u - 128)
                pix_u_g = - 0.391 * (pix_u - 128)
                pix_y2 = 1.164 * (pix_y2-16)
                pix_v_g = - 0.813 * (pix_v - 128)
                pix_v_r = 1.596 * (pix_v - 128)


                if self._data_['y'] == 0:
                    pix_y1 = 0
                    pix_y2 = 0
                if self._data_['u'] == 0:
                    pix_u_b = 0
                    pix_u_g = 0
                if self._data_['v'] == 0:
                    pix_v_g = 0
                    pix_v_r = 0

                blue = pix_y1 + pix_u_b
                green = pix_y1 + pix_v_g + pix_u_g
                red = pix_y1 + pix_v_r
                pix[j*2, i] = int(red), int(green), int(blue)

                blue = pix_y2 + pix_u_b
                green = pix_y2 + pix_v_g + pix_u_g
                red = pix_y2 + pix_v_r
                pix[j*2+1, i] = int(red), int(green), int(blue)
"""
