import tkinter as tk

class MyApplication:
    def __init__(self):
        # 윈도우 초기화
        self.window = tk.Tk()
        self.window.title("Tkinter Basic Button")  # 상단 제목 설정
        self.window.geometry("320x240+50+50")  # 지오메트리: 너비x높이+x좌표+y좌표
        # self.window.resizable(False, False)  # x축, y축 크기 조정 비활성화 (필요시 주석 해제)
        
        # UI 구성요소 생성
        self.create_widgets()
        
    def create_widgets(self):
        # 라벨 생성
        self.label = tk.Label(self.window, text="Hello")
        self.label.grid(column=0, row=0, padx=10, pady=10)
        
        # 버튼 생성
        self.button = tk.Button(
            self.window, 
            text='Click Me', 
            command=self.on_first_click
        )
        self.button.grid(column=1, row=0, padx=10, pady=10)
    
    def on_first_click(self):
        """첫 번째 클릭 동작"""
        self.label.config(text="world clicked!")
        self.button.config(command=self.on_second_click)
    
    def on_second_click(self):
        """두 번째 클릭 동작"""
        self.label.config(text="hello clicked!")
        self.button.config(command=self.on_first_click)
    
    def run(self):
        """애플리케이션 실행"""
        self.window.mainloop()


if __name__ == "__main__":
    app = MyApplication()
    app.run()