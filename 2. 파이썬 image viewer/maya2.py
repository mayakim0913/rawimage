#필요한 python 모듈과 pyside 모듈을 임포트 한다.
import sys
from PySide.QtGui import QApplication, QWidget

#QWIdget 클래스를 상속하는 클래스를 정의한다.
#QWidget 은 모든 ui 클래스의 베이스 클래스 이므로 보통 이를 상속해서 윈도우를 만들면 된다.
class MyWidget(QWidget):

    #생성자 메소드(__init__) 울 작성
    #생성자는 일반적으로 인스턴스 멤버를 생성하고 값을 초기화하는 데 사용된다.
    #여기서 슈퍼클래스인 QWidget의 생성자를 명시적으로 호출하여 다음과 같이 초기화해준다.
    def __init__(self):
        super(MyWidget, self).__init__()  #qwidget.__init__(self)

def main():
    #pyside는 반드시 하나의 메인 어플을 객체로 가져야 하므로 QApplication 인스탄스를 생성함
    #이때 넘기는 sys.argv 는 파이썬 스크립트가 캐맨드 라인으로부터 받는 인자 리스트인데,
    #첫번째 인자인 argv[0]에는 실행된 파이썬 스크립트 파일 이름이 자동으로 전달된다.
    app = QApplication(sys.argv)
    #앞에서 정의한 MyWidget클래스의 인스턴스 생성
    #show()메소드를 이용해 윈도우에 보여준다.
    win = MyWidget()
    win.show()
    #app.exec_()를 로출하면 메인 이벤트 루프에 진입해서 본격적으로 코드 실행 되고,
    #프로그램이 종료될 때 까지 무한 루프상태로 들어감
    sys.exit(app.exec_())

#파이썬 인터프리터에 의해 가장 먼저 실해되는 모듈은 __main__ 이라는 이름을 가지게 된다.
#즉, 지금까지 작성한 프로그램을 ~~.py라고 이름을 저장하고 이 파일(모듈)을 실행하면 모듈의 이름이 ~~ 이 아니라 __main__ 으로 해석한다.
#이는 독립적으로 실행 된 경우 이고, 다른 모듈에 의해 import되면 원래 이름인 ~~로 실행 된다.
if __name__ == '__main__':
    main()

