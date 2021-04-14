# 참고 : https://blog.xcoda.net/104

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton ,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QImage,QPixmap

import cv2
import threading

class MyApp(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        label = QLabel()
        self.label = label
        self.btn_start = QPushButton("Camera On")
        self.btn_stop = QPushButton("Camera Off")
        vbox.addWidget(label)
        vbox.addWidget(self.btn_start)
        vbox.addWidget(self.btn_stop)
        self.setLayout(vbox)
        self.show()

        self.aboutToQuit.connect(self.onExit)
        self.btn_start.clicked.connect(self._start)
        self.btn_stop.clicked.connect(self._stop)
        

    def _appLoop(self) :
        # self.running
        cap = cv2.VideoCapture(0)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.label.resize(width, height)
        while self.running:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                h,w,c = img.shape
                qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                label.setPixmap(pixmap)
            else:
                QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
    print("Thread end.")

    def _start(self):
        self.running = True
        th = threading.Thread(target=self._appLoop)
        th.start()
        print('thread start')
    def _stop(self):
        self.running = False
    def onExit(self) :
        self._stop()
        print('exit')

if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())