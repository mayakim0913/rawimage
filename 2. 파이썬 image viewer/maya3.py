import sys
from PySide.QtGui import QApplication, QWidget

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

def main():
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()