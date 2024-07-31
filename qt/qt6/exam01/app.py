import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('layout.ui', self)  # 여기에 실제 .ui 파일 이름을 넣으세요
        
        # 버튼 클릭 이벤트와 함수 연결
        self.btn_Test.clicked.connect(self.on_btn_test_clicked)

    def on_btn_test_clicked(self):
        # 버튼 클릭 시 라벨 텍스트 변경
        self.test_label.setText("Hello Qt")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다