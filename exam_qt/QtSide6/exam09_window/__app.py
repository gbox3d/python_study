import sys

from PySide6.QtUiTools import QUiLoader
from PySide6 import QtWidgets, QtUiTools
from PySide6.QtCore import QFile, QThread, Signal


UIloader = QtUiTools.QUiLoader()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            ui_file = QFile("layout_main.ui")
            if not ui_file.open(QFile.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            self.ui = UIloader.load(ui_file, self)
            ui_file.close()
            if not self.ui:
                print(UIloader.errorString())
                sys.exit(-1)
                
                #크기 지정
            self.setGeometry(self.ui.rect())
                
            # 메뉴바 설정
            if self.ui.menuBar():
                self.setMenuBar(self.ui.menuBar())
            
            # 상태바 설정
            if self.ui.statusBar():
                self.setStatusBar(self.ui.statusBar())
            
            # 중앙 위젯 설정
            if self.ui.centralWidget():
                self.setCentralWidget(self.ui.centralWidget())
                
            
            
            # # 도구 모음 설정
            # for toolbar in self.ui.findChildren(QtWidgets.QToolBar):
            #     self.addToolBar(toolbar)
            # # self.setCentralWidget(self.ui)
            
            
            
        except Exception as e:
            print(f"Error loading image: {e}")
            sys.exit(-1)
            
    def closeEvent(self, event):
        # 창이 닫히기 전에 호출되는 이벤트
        print("closeEvent")
        super().closeEvent(event)
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다