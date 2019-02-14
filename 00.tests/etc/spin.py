#!/usr/bin/env python3


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



class MainWindow(QMainWindow):
    count = 0
    def __init__(self):
	QMainWindow.__init__(self)
	self.start()


    def start(self):
        listDockWidget = QDockWidget("LIST Dock", self)
        listDockWidget.setObjectName("ListDockWidget")
        self.listWidget = QListWidget()
        listDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, listDockWidget)
 
        self.listWidget.addItems(["LIST FEATURES {}".format(k) 
                                    for k in range(1, 5)])

        # Image Label Dock Widget
        imageLabelDock = QDockWidget("IMAGE Dock", self)
        imageLabelDock.setObjectName("TextBrowserDockWidget")
        self.imageLabel = QLabel()
        imageLabelDock.setWidget(self.imageLabel)
        self.addDockWidget(Qt.BottomDockWidgetArea, imageLabelDock)
 
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFrameShape(QFrame.StyledPanel)
 
        self.image = QImage("/home/maya/rawimage/v1/icon/help.png") #:kubuntuLogoIcon.png")
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))

# Open Image Action
        openImageAction = QAction("OPEN IMAGE", self)
        openImageAction.setShortcut("Ctrl+I")
        openImageHelp = "OPEN IMAGE@@@@"
        openImageAction.setToolTip(openImageHelp)
        openImageAction.setStatusTip(openImageHelp)
	self.openImageAction.triggered.connect(self.OpenImage)
        #self.connect(openImageAction, SIGNAL("triggered()"), self.OpenImage)
 
        # Image Zoom Action
        imageZoomAction = QAction("IMAGE ZOOM IN/OUT", self)
        imageZoomHelp = "IN OUT!!!."
        imageZoomAction.setToolTip(imageZoomHelp)
        imageZoomAction.setStatusTip(imageZoomHelp)
	self.imageZoomAction.triggered.connect(self.ImageZoom)
        #self.connect(imageZoomAction, SIGNAL("triggered()"), self.ImageZoom)

# Image Label in Dock
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.imageLabel.addAction(openImageAction)
        self.imageLabel.addAction(imageZoomAction)


    def OpenImage(self):
        imageFormats = ["{0} file (*.{0})".format(ext.data().decode()) for ext in
                        QImageReader.supportedImageFormats()]
        imageFormats.append("all files (*.*)")
        fileDialog = QFileDialog(self, "open image", ".")
        fileDialog.setFilters(imageFormats)
        fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        if fileDialog.exec_():
            imageLink = fileDialog.selectedFiles()[0]
            self.image = QImage(imageLink)
            self.imageLabel.setPixmap(QPixmap.fromImage(self.image))


    def ImageZoom(self):
	if self.image.isNull():
		return 

        zoomDialog = QDialog(self)
 
        widthSpinBox = QSpinBox()
        widthSpinBox.setRange(0, 1000)
        widthSpinBox.setSuffix(" %")
        heightSpinBox = QSpinBox()
        heightSpinBox.setRange(0, 1000)
        heightSpinBox.setSuffix(" %")
         
        from math import ceil
        image = self.imageLabel.pixmap().toImage()
        widthZoom = ceil(image.width() * 100 / self.image.width())
        heightZoom = ceil(image.height() * 100 / self.image.height())
        widthSpinBox.setValue(widthZoom)
        heightSpinBox.setValue(heightZoom)
 
        sameZoomCheck = QCheckBox("maintain ratio!!!")
 

        def ValueSameSet(value):
            if sameZoomCheck.isChecked():
                widthSpinBox.setValue(value)
                heightSpinBox.setValue(value)
         
        self.connect(widthSpinBox, SIGNAL("valueChanged(int)"),        
                        ValueSameSet)
        self.connect(heightSpinBox, SIGNAL("valueChanged(int)"),
                        ValueSameSet)
        self.connect(sameZoomCheck, SIGNAL("stateChanged(int)"),
                    lambda: ValueSameSet(widthSpinBox.value()))
         
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | 
                                        QDialogButtonBox.Cancel)
        self.connect(buttonBox, SIGNAL("accepted()"), zoomDialog,
                        SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"), zoomDialog,
                        SLOT("reject()"))
 
        layout = QFormLayout()
        layout.addRow(QLabel("w: "), widthSpinBox)
        layout.addRow(QLabel("h: "), heightSpinBox)
        layout.addWidget(sameZoomCheck)
        layout.addWidget(buttonBox)
 
        zoomDialog.setLayout(layout)
        zoomDialog.setWindowTitle("in & out")
 
        if zoomDialog.exec_():
            widthZoom = widthSpinBox.value()
            heightZoom = heightSpinBox.value()
            width = self.image.width() * widthZoom / 100
            height = self.image.height() * heightZoom / 100
            image = self.image.scaled(width, height)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))




if __name__ == '__main__':                                          
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow() 
    MainWindow.setWindowTitle('Raw Image viewer')
    MainWindow.show()
    sys.exit(app.exec_())


