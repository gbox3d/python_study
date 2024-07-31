import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class MyApp(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()
    def initUI(self) :
        label = QLabel('hello',self)
        label.move(20,20)
        self.test_label = label

        _button = QPushButton('test',self)
        _button.move(80,13)
        _button.clicked.connect(self.clickBtn) # 핸들러 등록 

        self.setWindowTitle('exam2')
        self.setGeometry(300,300,320,240)
        self.show()

    # 이벤트 핸들러 
    def clickBtn(self) :
        self.test_label.setText('click')

if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
