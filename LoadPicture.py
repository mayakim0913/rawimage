import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
