import tkinter as tk
from tkinter import ttk

class FreqFrame(ttk.Frame):
    """목소리 주파수 범위 설정 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, padding=10)
        self.app = app
        self.detector = app.detector
        
        ttk.Label(self, text="사람 목소리 주파수 범위 (Hz)", style='Header.TLabel').grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 5))
        
        # 낮은 주파수 설정
        ttk.Label(self, text="하한 주파수:", style='Status.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_low = tk.IntVar(value=self.detector.human_freq_low)
        self.freq_low_scale = ttk.Scale(self, from_=50, to=200, variable=self.freq_low, orient=tk.HORIZONTAL, length=150, command=self.update_freq_low)
        self.freq_low_scale.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        self.freq_low_label = ttk.Label(self, text=f"{self.detector.human_freq_low} Hz", style='Status.TLabel')
        self.freq_low_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 높은 주파수 설정
        ttk.Label(self, text="상한 주파수:", style='Status.TLabel').grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_high = tk.IntVar(value=self.detector.human_freq_high)
        self.freq_high_scale = ttk.Scale(self, from_=200, to=400, variable=self.freq_high, orient=tk.HORIZONTAL, length=150, command=self.update_freq_high)
        self.freq_high_scale.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        self.freq_high_label = ttk.Label(self, text=f"{self.detector.human_freq_high} Hz", style='Status.TLabel')
        self.freq_high_label.grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 주파수 관련 위젯 저장 (활성화/비활성화를 위해)
        self.freq_widgets = [self.freq_low_scale, self.freq_high_scale, self.freq_low_label, self.freq_high_label]
        
        # 안내 메시지
        ttk.Label(self, text="일반적인 성인 목소리: 85~255 Hz", 
                font=(self.app.font_family, 8, 'italic')).grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(10, 0))
        ttk.Label(self, text="어린이 목소리: 130~400 Hz", 
                font=(self.app.font_family, 8, 'italic')).grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5, pady=0)
        ttk.Label(self, text="소음(기계, 바람 등): 주로 50~100 Hz 이하 또는 300 Hz 이상", 
                font=(self.app.font_family, 8, 'italic')).grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=5, pady=0)
    
    def update_freq_low(self, event=None):
        """하한 주파수 업데이트"""
        value = int(self.freq_low.get())
        # 상한 주파수를 초과하지 않도록 제한
        high_value = self.freq_high.get()
        if value >= high_value:
            value = high_value - 1
            self.freq_low.set(value)
            
        self.detector.human_freq_low = value
        self.freq_low_label.config(text=f"{value} Hz")
    
    def update_freq_high(self, event=None):
        """상한 주파수 업데이트"""
        value = int(self.freq_high.get())
        # 하한 주파수 미만이 되지 않도록 제한
        low_value = self.freq_low.get()
        if value <= low_value:
            value = low_value + 1
            self.freq_high.set(value)
            
        self.detector.human_freq_high = value
        self.freq_high_label.config(text=f"{value} Hz")