from PySide import QtCore, QtGui 
import sys
import platform


class MainWindowWidget(QtGui.QWidget):


    def __init__(self):
        super(MainWindowWidget, self).__init__()

        # Button that allows loading of images
        self.load_button = QtGui.QPushButton("Load image")
        self.load_button.clicked.connect(self.load_image_but)

        # Image viewing region
        self.lbl = QtGui.QLabel(self)

        # A horizontal layout to include the button on the left
        layout_button = QtGui.QHBoxLayout()
        layout_button.addWidget(self.load_button)
        layout_button.addStretch()

        # A Vertical layout to include the button layout and then the image
        layout = QtGui.QVBoxLayout()
        layout.addLayout(layout_button)
        layout.addWidget(self.lbl)

        self.setLayout(layout)

        # Enable dragging and dropping onto the GUIi
#        self.setAcceptDrops(True)

        self.show()

    def load_image_but(self):

        #Get the file location
        self.fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        # Load the image from the location
        self.load_image()

    def load_image(self):
        """
        Set the image to the pixmap
        :return:
        """
        pixmap = QtGui.QPixmap(self.fname)
        pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        self.lbl.setPixmap(pixmap)



# Run if called directly
if __name__ == '__main__':
    # Initialise the application
    app = QtGui.QApplication(sys.argv)
    # Call the widget
    ex = MainWindowWidget()
    sys.exit(app.exec_())
