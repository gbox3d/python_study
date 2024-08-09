import sys
from PySide6.QtWidgets import QApplication, QWidget

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

import PySide6
import pyqtgraph as pg
pg.setConfigOption('useOpenGL', True)  # 선택사항: OpenGL 사용 (성능 향상을 위해)
pg.setConfigOption('foreground', 'k')  # 선택사항: 전경색 설정
pg.setConfigOption('background', 'w')  # 선택사항: 배경색 설정

UIloader = QUiLoader()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        try :
            ui_file = QFile("layout_main.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            
            self.ui = UIloader.load(ui_file,self) # self를 넣어줘야 ui 파일에서 정의한 위젯을 사용할 수 있음
            ui_file.close()
            
            if not self.ui:
                print(UIloader.errorString())
                sys.exit(-1)
                
            # 그래프 생성
            # pyqtgraph 플롯 위젯 생성
            plot_widget = pg.PlotWidget(self.ui.widgetPlotGraph)
            
            # 플롯 위젯 크기 설정
            plot_widget.setGeometry(self.ui.widgetPlotGraph.rect())
            
            # 데이터 플로팅
            x = [0, 1, 2, 3, 4, 5]
            y = [0, 1, 4, 9, 16, 25]
            plot_widget.plot(x, y, pen='r')
            
                
        except Exception as e:
                print(f"Error loading image: {e}")
                sys.exit(-1)
    def closeEvent(self, event):
        # 창이 닫히기 전에 호출되는 이벤트
        print("closeEvent")
        super().closeEvent(event)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다