import tkinter as tk
from tkinter import ttk

class StatusFrame(ttk.Frame):
    """음성 감지 상태 표시 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, style='LightBlue.TFrame', padding=10)
        self.app = app
        
        ttk.Label(self, text="음성 감지 상태", style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 감지 상태 지표들
        ttk.Label(self, text="VAD 결과:", style='Status.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.vad_result = ttk.Label(self, text="N/A", style='Status.TLabel')
        self.vad_result.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self, text="RMS 값:", style='Status.TLabel').grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.rms_value = ttk.Label(self, text="N/A", style='Status.TLabel')
        self.rms_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self, text="주파수 분석 결과:", style='Status.TLabel').grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_result = ttk.Label(self, text="N/A", style='Status.TLabel')
        self.freq_result.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self, text="연속 음성 프레임:", style='Status.TLabel').grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.speech_frames = ttk.Label(self, text="N/A", style='Status.TLabel')
        self.speech_frames.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self, text="최종 판정:", style='Status.TLabel').grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.final_decision = ttk.Label(self, text="N/A", style='Status.TLabel')
        self.final_decision.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 상태 표시등
        ttk.Label(self, text="현재 상태:", style='Status.TLabel').grid(row=1, column=2, sticky=tk.E, padx=5, pady=2)
        self.status_indicator = tk.Canvas(self, width=30, height=30, bg='white', highlightthickness=0)
        self.status_indicator.grid(row=1, column=3, padx=5, pady=2)
        self.status_indicator.create_oval(5, 5, 25, 25, fill='gray', outline='')
    
    def update_ui(self, vad, rms, freq, speech_count, is_continuous, speech_detected):
        """UI 요소 업데이트"""
        # 애플리케이션이 종료 중이면 업데이트 중단
        if self.app.is_closing:
            return
            
        # UI 위젯이 아직 존재하는지 확인
        try:
            self.vad_result.config(text=f"{'검출됨' if vad else '검출 안됨'}")
            self.rms_value.config(text=f"{rms:.1f} / {self.app.detector.VOICE_THRESHOLD:.1f}")
            self.freq_result.config(text=f"{'검출됨' if freq else '검출 안됨'}")
            self.speech_frames.config(text=f"{speech_count} / {self.app.detector.required_speech_frames}")
            
            # 최종 판정 및 표시등 업데이트
            if is_continuous:
                self.final_decision.config(text="음성 감지됨")
                self.status_indicator.itemconfig(1, fill='green')
            elif speech_detected:
                self.final_decision.config(text="음성 감지 중...")
                self.status_indicator.itemconfig(1, fill='yellow')
            else:
                self.final_decision.config(text="음성 없음")
                self.status_indicator.itemconfig(1, fill='red')
        except Exception as e:
            # 위젯이 이미 파괴된 경우 무시
            print(f"UI 업데이트 오류 (무시됨): {e}")
            return
    
    def reset_ui(self):
        """UI 상태 초기화"""
        self.vad_result.config(text="N/A")
        self.rms_value.config(text="N/A")
        self.freq_result.config(text="N/A")
        self.speech_frames.config(text="N/A")
        self.final_decision.config(text="N/A")
        self.status_indicator.itemconfig(1, fill='gray')