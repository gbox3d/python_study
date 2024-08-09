import sys
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        ui_file = QFile("layout_loginDlg.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
            sys.exit(-1)
        
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        if not self.ui:
            print(loader.errorString())
            sys.exit(-1)
            
        # Connect the buttonBox signals to our custom slots
        self.ui.buttonBox.accepted.connect(self.on_accepted)
        self.ui.buttonBox.rejected.connect(self.on_rejected)
            
        self.ui.show()
        
    def on_accepted(self):
        print("확인 버튼이 클릭되었습니다.")
        self.ui.accept()
    
    def on_rejected(self):
        print("취소 버튼이 클릭되었습니다.")
        self.ui.reject()