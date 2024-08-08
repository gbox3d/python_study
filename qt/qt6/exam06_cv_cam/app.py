import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice,Signal,Qt,QTimer,QSize  
from PySide6.QtWidgets import QApplication, QWidget,QPushButton,QLabel,QVBoxLayout,QSizePolicy
from PySide6.QtGui import QImage, QPixmap

import cv2

        
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
              
            # print(f" Scaled Contents :{self.ui.imgView.hasScaledContents()} ")  
            
            # Initialize webcam
            self.cap = cv2.VideoCapture(0)
            
            # Create a timer to update the webcam feed
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # Update every 30 ms (approximately 33 fps)
            
            self.ui.show()
            
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
        
        
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())