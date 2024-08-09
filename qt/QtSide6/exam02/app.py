import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, QIODevice


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        try :
            ui_file = QFile("layout.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            loader = QUiLoader()
            self.ui = loader.load(ui_file,self)
            ui_file.close()

            if not self.ui:
                print(loader.errorString())
                sys.exit(-1)
                
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())