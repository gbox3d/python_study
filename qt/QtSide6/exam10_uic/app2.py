from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import loadUiType

app = QApplication([])

Ui_MainWindow, QMainWindow = loadUiType('layout.ui')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

window = MainWindow()
window.show()
app.exec()
