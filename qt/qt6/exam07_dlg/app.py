import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication, QWidget, QDialog ,QLabel,QVBoxLayout

from PySide6.QtGui import QPixmap

from aboutDlg import AboutDlg

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        try :
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
                
                
            self.ui.btnAbout.clicked.connect(self.onClickAbout)
            
            # suenaga_ouka.png 파일에서 직접 pixmap을 생성하여 QLabel에 표시
            image_file = "suenaga_ouka.png"
            try:
            # 이미지 파일을 직접 QPixmap으로 로드
                pixmap = QPixmap(image_file)
                
                if pixmap.isNull():
                    print(f"Failed to load image: {image_file}")
                    return
                
                _imgLabel = QLabel()
                _imgLabel.setPixmap(pixmap)
                _imgLabel.setScaledContents(True)
                
                # _imgLabel.setFixedSize(200, 200)
                
                # widgetImg에 레이아웃이 없다면 새로 생성
                # layout = self.ui.widgetImg.layout()
                if self.ui.widgetImg.layout() is None:
                    layout = QVBoxLayout()
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.ui.widgetImg.setLayout(layout)
                
                # 새 라벨 추가
                self.ui.widgetImg.layout().addWidget(_imgLabel)
                
                # QLabel에 이미지 설정
                # self.ui.widgetImg.setPixmap(pixmap)
                # self.ui.widgetImg.setScaledContents(True)
                print(f"Successfully loaded and displayed image: {image_file}")
            
            except Exception as e:
                print(f"Error loading image: {e}")
                
            self.ui.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
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
    sys.exit(app.exec())  # PyQt6에서는 exec_() 대신 exec()를 사용합니다