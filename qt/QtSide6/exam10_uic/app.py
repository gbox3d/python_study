import sys
from PySide6.QtWidgets import QApplication, QWidget
from layout import Ui_Form

class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 여기에 버튼 클릭 등의 이벤트 핸들러를 추가할 수 있습니다.
        self.btnTest.clicked.connect(self.on_button_clicked)
    
    def on_button_clicked(self):
        print("버튼이 클릭되었습니다!")
        self.lbTest.setText("버튼이 클릭되었습니다!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())