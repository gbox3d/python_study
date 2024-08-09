import sys

from PySide6  import __version__ as PySide6_version
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication,QWidget


UIloader = QUiLoader()

print(f"PySide6 version: {PySide6_version}")
# print(f"Qt version: {qVersion()}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        try :
            ui_file = QFile("layout.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            
            self.ui = UIloader.load(ui_file,self) # self를 넣어줘야 ui 파일에서 정의한 위젯을 사용할 수 있음
            ui_file.close()
            
            if not self.ui:
                print(UIloader.errorString())
                sys.exit(-1)
            
            self.ui.btn_Test.clicked.connect(self.on_btn_test_clicked)
            
            # self.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")

    def on_btn_test_clicked(self):
        # 버튼 클릭 시 라벨 텍스트 변경
        self.ui.test_label.setText("Hello Qt")
        
    def closeEvent(self, event):
        # 창이 닫히기 전에 호출되는 이벤트
        print("closeEvent")
        super().closeEvent(event)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다