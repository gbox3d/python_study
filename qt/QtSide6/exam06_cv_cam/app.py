import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice,Signal,Qt,QTimer,QSize,QEvent
from PySide6.QtWidgets import QApplication, QWidget,QPushButton,QLabel,QVBoxLayout,QSizePolicy
from PySide6.QtGui import QImage, QPixmap

import cv2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        try:
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
                
            self.ui.imgView = QLabel(self.ui.widgetCamView)
            self.ui.imgView.setScaledContents(True) # 이미지 라벨의 크기를 위젯의 크기에 맞게 조정
            self.ui.imgView.setGeometry(self.ui.widgetCamView.rect()) # 위젯의 크기에 맞게 이미지 라벨의 크기를 조정
            
            # Initialize webcam
            self.cap = cv2.VideoCapture(0)
            
            # Create a timer to update the webcam feed
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # Update every 30 ms (approximately 33 fps)
            
            # self.ui.closeEvent = self.closeEvent
            # self.ui.setParent(self)
            # self.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the image from BGR to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            
            # Convert the image to Qt format
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.imgView.setPixmap(pixmap) # Scaled Contents 가 True 이기 문에 따로 크기조정이 필요없다.
    
    def closeEvent(self, event):
        # Release the camera when closing the application
        self.cap.release()
        super().closeEvent(event)
        
        print("Camera released")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())