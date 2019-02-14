import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from MainGUI import *
from main import *


class LogObject(QObject):
    MousePixmapSignal = pyqtSignal(QPoint, QColor)


class PictureItem(QGraphicsPixmapItem):
    def __init__(self, log, *args, **kwargs):
        QGraphicsPixmapItem.__init__(self, *args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.log = log

    def hoverMoveEvent(self, event):
        point = event.pos().toPoint()
        color = QColor(self.pixmap().toImage().pixel(point.x(), point.y()))
        self.log.MousePixmapSignal.emit(point, color)
        QGraphicsPixmapItem.hoverMoveEvent(self, event)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CrossCursor)
        QGraphicsPixmapItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        QGraphicsPixmapItem.hoverLeaveEvent(self, event)


class LoadPicture(QWidget):
    def __init__(self, pixmap, parent=None):
        QWidget.__init__(self, parent)     
	self.setupUi(self)	
        self.log = LogObject(self)
        self.PictureArea.setScene(QGraphicsScene())
        self.item = PictureItem(self.log, pixmap)
        self.PictureArea.scene().addItem(self.item)
      #  self.resize(pixmap.size())

    def setupUi(self, GraphicsArea):
        GraphicsArea.setObjectName("GraphicsArea")
      #  GraphicsArea.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(GraphicsArea)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(GraphicsArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.PictureArea = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents)
        self.PictureArea.setObjectName("PictureArea")
        self.gridLayout_2.addWidget(self.PictureArea, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(GraphicsArea)
        QtCore.QMetaObject.connectSlotsByName(GraphicsArea)

    def retranslateUi(self, GraphicsArea):
        _translate = QtCore.QCoreApplication.translate
        GraphicsArea.setWindowTitle(_translate("GraphicsArea", "Form"))


    def setUpLoadInputUi(self):
        pass
        self.scene=QGraphicsScene()
        self.pixitem=QGraphicsPixmapItem()
        self.grali=[]


    def setpicture(self,pixmap):
        self.pixitem.setPixmap(pixmap)
        self.grali.append(self.pixitem)
        self.scene.addItem(self.grali[-1])
        self.GraphicAreaGUI.PictureArea.setScene(self.scene)
        self.GraphicAreaGUI.PictureArea.show()
        self.GraphicAreaGUI.PictureArea.setMouseTracking(True)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseMove and
            source is self.GraphicAreaGUI.PictureArea.viewport()):
            self.MousePositionSignal.emit(event)
        return QWidget.eventFilter(self, source, event)




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

