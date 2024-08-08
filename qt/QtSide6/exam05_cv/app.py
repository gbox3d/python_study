import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile, QIODevice,Signal,Qt
from PySide6.QtWidgets import QPushButton, QLabel,QGraphicsView,QGraphicsScene
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
                
            # self.CVImageView = self.ui.CVImageView
            # self.graphics_scene = QGraphicsScene(self.CVImageView)
            # self.CVImageView.setScene(self.graphics_scene)
            
            image_path = "fukuda.jpg"
            
            cv_img = cv2.imread(image_path)
            
            # Convert the image from BGR to RGB
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            
            #CVImageView 크기에 맞게 이미지 크기 조정
            # _width = self.CVImageView.width()
            # _height = self.CVImageView.height()
            # rgb_image = cv2.resize(rgb_image, (_width, _height))
            
            # Convert the image to Qt format
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Create a pixmap from the QImage
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.imgView.setPixmap(pixmap)
            
            self.ui.show()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the file name of the .ui file")
            
            
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())