import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, QIODevice,Signal
from PySide6.QtWidgets import QPushButton, QLabel
import _rc

        
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        try:
            ui_file = QFile("layout_main.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            loader = QUiLoader()
            self.ui = loader.load(ui_file)
            ui_file.close()

            if not self.ui:
                print(loader.errorString())
                sys.exit(-1)
            
            self.testBtn = self.ui.findChild(QPushButton, "testBtn")
            
            self.textout = self.ui.findChild(QLabel, "textout")
            
            self.testBtn.clicked.connect(self.onClick_imgBtn)
            
            self.ui.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
    def onClick_imgBtn(self):
        self.textout.setText("Hello Qt")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())