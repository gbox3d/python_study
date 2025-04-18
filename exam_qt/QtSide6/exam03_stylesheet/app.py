import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, QIODevice
import _rc

import os

UIloader = QUiLoader()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        try:
            
            print("Current directory:", os.getcwd())

            ui_file = QFile("layout_main.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            
            self.ui = UIloader.load(ui_file,self)
            ui_file.close()

            if not self.ui:
                print(UIloader.errorString())
                sys.exit(-1)
            
            # self.ui.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())