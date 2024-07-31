import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        try:
        
            uic.loadUi('layout.ui', self)  # 여기에 실제 .ui 파일 이름을 넣으세요
            
        except AttributeError as e:
            print(f"Warning: {e}")
            print("Please check the file name of the .ui file")
            sys.exit(1)
            
            
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())