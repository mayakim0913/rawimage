import sys 
from PySide import QtGui

app = QtGui.QApplication(sys.argv)

a = QtGui.QWidget()
a.resize(250,150)
a.setWindowTitle('Simple')
a.show()

sys.exit(app.exec_())
