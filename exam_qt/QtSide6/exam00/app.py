import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # 창 크기 설정
        self.setGeometry(100, 100, 320, 240)
        self.setWindowTitle('Hello World App')

        # 수직 레이아웃 생성
        main_layout = QVBoxLayout()
        
         # "Hello World" 라벨 생성 및 설정
        hello_label = QLabel("Hello World")
        hello_label.setFont(QFont(self.font().family(), 24))  # 기본 폰트의 크기만 변경
        hello_label.setAlignment(Qt.AlignCenter)
        
        # "Hello World" 라벨을 메인 레이아웃에 추가
        main_layout.addWidget(hello_label)
        
        # 수평 레이아웃 생성
        input_layout = QHBoxLayout()
        
        # 이름 라벨 생성
        name_label = QLabel("이름:")
        input_layout.addWidget(name_label)
        
        # 라인 에디트 생성
        self.name_input = QLineEdit()
        input_layout.addWidget(self.name_input)
        
        # 버튼 생성
        submit_button = QPushButton("확인")
        submit_button.clicked.connect(self.on_button_click)
        input_layout.addWidget(submit_button)
        
        # 수평 레이아웃을 메인 레이아웃에 추가
        main_layout.addLayout(input_layout)
        
        # 결과 출력을 위한 라벨 생성
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)
        
        # 수직 스페이서 추가
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 위젯에 메인 레이아웃 설정
        self.setLayout(main_layout)
        
    def on_button_click(self):
        name = self.name_input.text()
        if name:
            self.result_label.setText(f"Hello, {name}!")
        else:
            self.result_label.setText("이름을 입력해주세요.")
    
    def closeEvent(self, event):
        print("closeEvent")
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
     # 폰트 로드
    font_id = QFontDatabase.addApplicationFont(sys.path[0] + "/./DungGeunMo.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # 전체 애플리케이션의 폰트 설정
        app.setFont(QFont(font_family, 12))  # 기본 크기를 12로 설정
    else:
        print("Failed to load custom font. Using system default.")
        
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())