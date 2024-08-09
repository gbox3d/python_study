import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication, QWidget, QDialog ,QLabel,QVBoxLayout

from PySide6.QtGui import QPixmap

from aboutDlg import AboutDlg
from loginDlg import LoginDialog

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        try :
            ui_file = QFile("layout_main.ui")
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
                sys.exit(-1)
            
            loader = QUiLoader()
            self.ui = loader.load(ui_file,self)
            ui_file.close()

            if not self.ui:
                print(loader.errorString())
                sys.exit(-1)
                
                
            self.ui.btnAbout.clicked.connect(self.onClickAbout)
            
            # suenaga_ouka.png 파일에서 직접 pixmap을 생성하여 QLabel에 표시
            image_file = "suenaga_ouka.png"
            try:
            # 이미지 파일을 직접 QPixmap으로 로드
                pixmap = QPixmap(image_file)
                
                if pixmap.isNull():
                    print(f"Failed to load image: {image_file}")
                    return
                
                # _imgLabel = QLabel()
                # _imgLabel.setPixmap(pixmap)
                # _imgLabel.setScaledContents(True)
                
                # # widgetImg에 레이아웃이 없다면 새로 생성
                # if self.ui.widgetImg.layout() is None:
                #     layout = QVBoxLayout()
                #     layout.setContentsMargins(0, 0, 0, 0)
                #     self.ui.widgetImg.setLayout(layout)
                
                # # 새 라벨 추가
                # self.ui.widgetImg.layout().addWidget(_imgLabel)
                
                _imgLabel = QLabel(self.ui.widgetImg)
                _imgLabel.setPixmap(pixmap)
                _imgLabel.setScaledContents(True)

                # widgetImg의 크기에 맞춰 이미지 라벨의 크기 설정
                _imgLabel.setGeometry(self.ui.widgetImg.rect())

                # 필요하다면 widgetImg의 크기가 변경될 때 이미지 라벨의 크기도 조정
                # self.ui.widgetImg.resizeEvent = lambda event: _imgLabel.setGeometry(self.ui.widgetImg.rect())
                
                self.ui.btnLogin.clicked.connect(self.onClickLogin)
                
                # QLabel에 이미지 설정
                print(f"Successfully loaded and displayed image: {image_file}")
            
            except Exception as e:
                print(f"Error loading image: {e}")
                
            
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
    def onClickLogin(self):
        print("Login 버튼이 클릭되었습니다.")
        login_dialog = LoginDialog()
        result = login_dialog.ui.exec()
        
        if result == QDialog.Accepted:
            print("확인 버튼이 클릭되었습니다.")
            print("ID:", login_dialog.ui.edt_ID.text())
            print("Password:", login_dialog.ui.edt_Passwd.text())
            
            self.ui.lbOutput.setText(f"로그인 성공 \n ID: {login_dialog.ui.edt_ID.text()}")
            
            
            
        else:
            print("취소 버튼이 클릭되었습니다.")
            
    def onClickAbout(self):
        print("About 버튼이 클릭되었습니다.")
        about_dialog = AboutDlg()
        result = about_dialog.ui.exec()
        
        if result == QDialog.Accepted:
            print("확인 버튼이 클릭되었습니다.")
            
            
            
            
        else:
            print("취소 버튼이 클릭되었습니다.")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다