import tkinter as tk
from tkinter import messagebox

class MyApplication:
    def __init__(self):
        # 윈도우 초기화
        self.mainwindow = tk.Tk()
        self.mainwindow.title("내 Tkinter 애플리케이션")
        self.mainwindow.geometry("500x300")  # 윈도우 크기 설정 (너비x높이)
        
        # 종료 이벤트 처리 설정
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # GUI 요소 생성
        self.create_widgets()
        
        # 변수 초기화
        self.counter = 0
        
    def create_widgets(self):
        # 프레임 생성 (레이아웃 관리용)
        main_frame = tk.Frame(self.mainwindow, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목 레이블
        title_label = tk.Label(
            main_frame, 
            text="Tkinter 예제 애플리케이션", 
            font=("Helvetica", 16)
        )
        title_label.pack(pady=(0, 20))
        
        # 카운터 레이블
        self.count_label = tk.Label(
            main_frame,
            text="카운트: 0",
            font=("Helvetica", 12)
        )
        self.count_label.pack(pady=(0, 10))
        
        # 버튼 프레임
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # 증가 버튼
        increment_button = tk.Button(
            button_frame,
            text="증가",
            command=self.increment_counter,
            width=10
        )
        increment_button.pack(side=tk.LEFT, padx=5)
        
        # 감소 버튼
        decrement_button = tk.Button(
            button_frame,
            text="감소",
            command=self.decrement_counter,
            width=10
        )
        decrement_button.pack(side=tk.LEFT, padx=5)
        
        # 리셋 버튼
        reset_button = tk.Button(
            button_frame,
            text="리셋",
            command=self.reset_counter,
            width=10
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # 종료 버튼
        exit_button = tk.Button(
            main_frame,
            text="종료",
            command=self.on_closing,
            width=10
        )
        exit_button.pack(pady=20)
        
    def increment_counter(self):
        """카운터 증가 함수"""
        self.counter += 1
        self.update_counter_display()
        
    def decrement_counter(self):
        """카운터 감소 함수"""
        self.counter -= 1
        self.update_counter_display()
        
    def reset_counter(self):
        """카운터 리셋 함수"""
        self.counter = 0
        self.update_counter_display()
        
    def update_counter_display(self):
        """카운터 표시 업데이트"""
        self.count_label.config(text=f"카운트: {self.counter}")
        
    def on_closing(self):
        """창 닫기 이벤트 처리"""
        if messagebox.askokcancel("종료", "정말 종료하시겠습니까?"):
            self.mainwindow.destroy()

    def run(self):
        """애플리케이션 실행"""
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = MyApplication()
    app.run()