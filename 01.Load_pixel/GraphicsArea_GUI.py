from PyQt5 import QtCore, QtGui, QtWidgets

from LoadPicture import *
from MainWindow import *
from Main_GUI import *


class Ui_GraphicsArea(object):
    def setupUi(self, GraphicsArea):
        GraphicsArea.setObjectName("GraphicsArea")
        GraphicsArea.resize(400, 300)
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




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GraphicsArea = QtWidgets.QWidget()
    ui = Ui_GraphicsArea()
    ui.setupUi(GraphicsArea)
    GraphicsArea.show()
    sys.exit(app.exec_())

