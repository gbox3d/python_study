import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout
from PySide6.QtWidgets import QFileDialog, QGraphicsPixmapItem,QGraphicsItem
from PySide6.QtGui import QPen, QColor, QBrush, QCursor, QPainter,QPixmap
from PySide6.QtCore import QTimer, QLineF, QRectF, Qt, QPointF

import UI.MainWindow

class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        layout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(layout)

        self.view = QGraphicsView(self.centralwidget)
        layout.addWidget(self.view)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        
        # view 크기 얻기
        # self.view_size = self.view.size()
        print(self.centralwidget.size())

        # 장면의 크기 설정
        self.scene.setSceneRect(0,0,256,256)
        
        
        #씬영역 전체 칠하기
        self.scene.addRect(self.scene.sceneRect(), QPen(Qt.NoPen), QBrush(QColor(0, 0, 0)))
        
        print(self.scene.sceneRect())
        
        
        self.scene.addLine(0,self.scene.sceneRect().height()/2,self.scene.sceneRect().width(),self.scene.sceneRect().height()/2, QPen(Qt.yellow))
        self.scene.addLine(self.scene.sceneRect().width()/2,0,self.scene.sceneRect().width()/2,self.scene.sceneRect().height(), QPen(Qt.yellow))
        
        
        self.greenRect = self.scene.addRect(0,0,64,64, QPen(Qt.green))
        
        self.greenRect.setFlag(QGraphicsItem.ItemIsMovable)

        # 십자선 그리기
        # self.draw_crosshair()

        self.actionclear.triggered.connect(self.clear_scene)
        self.actionload.triggered.connect(self.load_scene)
        self.actionsave.triggered.connect(self.save_scene)
        self.actionline.triggered.connect(self.draw_random_line)
        self.actionrect.triggered.connect(self.draw_random_rectangle)
        
        self.actionimage.triggered.connect(self.load_image)

    # def draw_crosshair(self):
    #     # 십자선 색상 및 스타일 설정
    #     pen = QPen(QColor(0, 0, 0))  # 회색
    #     pen.setStyle(Qt.DashLine)  # 점선 스타일
    #     pen.setWidth(1)

    #     # 수평선 그리기
    #     line = QLineF(0,0, self.scene.sceneRect().left(), self.scene.sceneRect().top())
    #     self.scene.addLine(line, pen)
        
    #     # # 수직선 그리기
    #     # line = QLineF(0, self.scene.sceneRect().top()/2, 0, self.scene.sceneRect().bottom()/2)
    #     # self.scene.addLine(line, pen)

    def draw_random_line(self):
        scene_rect = self.scene.sceneRect()
        start_x = random.uniform(scene_rect.left(), scene_rect.right())
        start_y = random.uniform(scene_rect.top(), scene_rect.bottom())
        end_x = random.uniform(scene_rect.left(), scene_rect.right())
        end_y = random.uniform(scene_rect.top(), scene_rect.bottom())

        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        pen = QPen(color)
        line = QLineF(start_x, start_y, end_x, end_y)
        self.scene.addLine(line, pen)

    def draw_random_rectangle(self):
        scene_rect = self.scene.sceneRect()
        x = random.uniform(scene_rect.left(), scene_rect.right())
        y = random.uniform(scene_rect.top(), scene_rect.bottom())

        width = random.uniform(scene_rect.width() * 0.05, scene_rect.width() * 0.15)
        height = random.uniform(scene_rect.height() * 0.05, scene_rect.height() * 0.15)

        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        rect = QRectF(x, y, width, height)
        pen = QPen(color)
        brush = QBrush(color)
        _rect = self.scene.addRect(rect, pen, brush)
        
        _rect.setFlag(QGraphicsItem.ItemIsMovable)
        
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            if not pixmap.isNull():
                # 이미지 크기 조정 (선택사항)
                max_size = 300  # 최대 너비 또는 높이
                if pixmap.width() > max_size or pixmap.height() > max_size:
                    pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # QGraphicsPixmapItem을 생성하고 씬에 추가
                item = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(item)
                
                # 이미지를 씬의 중앙에 배치
                item_pos = QPointF(self.scene.width()/2 - pixmap.width()/2,
                                   self.scene.height()/2 - pixmap.height()/2)
                item.setPos(item_pos)
                
                
                item.setFlag(QGraphicsItem.ItemIsMovable)


    def clear_scene(self):
        self.scene.clear()
        self.draw_crosshair()  # 십자선 다시 그리기

    def load_scene(self):
        pass

    def save_scene(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())