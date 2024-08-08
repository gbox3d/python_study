import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        try :
            ui_file = QFile("layout.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            loader = QUiLoader()
            self.ui = loader.load(ui_file)
            ui_file.close()

            if not self.ui:
                print(loader.errorString())
                sys.exit(-1)
            
            self.ui.btn_Test.clicked.connect(self.on_btn_test_clicked)
                
            # self.test_label = self.ui.findChild(QLabel, "test_label")
            # self.btn_Test = self.ui.findChild(QPushButton, "btn_Test")
            
            #  # 버튼 클릭 이벤트와 함수 연결
            # if self.btn_Test:
            #     self.btn_Test.clicked.connect(self.on_btn_test_clicked)
            # else:
            #     print("Button 'btn_Test' not found")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")

    def on_btn_test_clicked(self):
        # 버튼 클릭 시 라벨 텍스트 변경
        self.ui.test_label.setText("Hello Qt")
    def show(self):
        self.ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다