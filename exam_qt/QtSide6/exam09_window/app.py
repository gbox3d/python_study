import sys
from PySide6.QtWidgets import QApplication ,QMainWindow
from layout_main import Ui_MainWindow


class MainWindow( QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def closeEvent(self, event):
        # 창이 닫히기 전에 호출되는 이벤트
        print("closeEvent")
        super().closeEvent(event)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())