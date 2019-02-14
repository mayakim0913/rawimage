import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Main_GUI import *
from GraphicsArea_GUI import *
from LoadPicture import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setUpMainUiFunction()

    def setUpMainUiFunction(self):
        self.actionOpen.triggered.connect(self.OpenDialog)
        self.Button_LoadPhoto.clicked.connect(self.OpenDialog)

        open = QAction(QIcon("icons/open.bmp"), "open", self)
        save = QAction(QIcon("icons/save.bmp"), "save", self)
        NormalCursor = QAction(QIcon("icons/cursor-normal.png"), "NormalCursor", self)
        CrosshairCursor = QAction(QIcon("icons/crosshair.png"), "CrosshairCursor", self)

        self.TopToolBar.addAction(open)
        self.TopToolBar.addAction(save)
        self.LeftToolBar.addAction(NormalCursor)
        self.LeftToolBar.addAction(CrosshairCursor)

        # self.TopToolBar.actionTriggered[QAction].connect(self.toolbtnpressed)

    def OpenDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        PicturePath = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", PicturePath, "JPEG File (*.png)", options=options)
        for filename in filenames:
            pixmap = QPixmap(filename)
            self.showPicture(pixmap)
            self.statusbar.showMessage("Successfully Loaded: {}".format(filename))

    def showPicture(self, picture):
        sub = QMdiSubWindow(self)
        loadPicture = LoadPicture(picture, sub)
        sub.setWidget(loadPicture)
        sub.setObjectName("Load_Picture_window")
        sub.setWindowTitle("New Photo")
        self.mdiArea.addSubWindow(sub)
        sub.show()
        sub.resize(picture.size())
        loadPicture.log.MousePixmapSignal.connect(self.updatePixel)

    def updatePixel(self, point, color):
        self.UserInput_PixelValue_X.setText("{}".format(point.x()))
        self.UserInput_PixelValue_Y.setText("{}".format(point.y()))

        self.UserInput_PixelValue_R.setText("{}".format(color.red()))
        self.UserInput_PixelValue_G.setText("{}".format(color.green()))
        self.UserInput_PixelValue_B.setText("{}".format(color.blue()))

if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    pyqtRemoveInputHook()
    app = QtWidgets.QApplication(sys.argv)
#    app.setAttribute(Qt.AA_EnableHighDpiScaling,True)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width()/1.5, screen_resolution.height()/1.2
    MainWindow = MainWindow()
    MainWindow.resize(width,height)
    MainWindow.setWindowTitle('Figure out name later')
    MainWindow.show()
    sys.exit(app.exec_())
