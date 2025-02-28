import tkinter as tk
from tkinter import ttk, messagebox

class ParamFrame(ttk.Frame):
    """감지 파라미터 설정 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, padding=10)
        self.app = app
        self.detector = app.detector
        
        ttk.Label(self, text="감지 파라미터 설정", style='Header.TLabel').grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 5))
        
        # VAD 모드 설정
        ttk.Label(self, text="VAD 모드:", style='Status.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.vad_mode = tk.IntVar(value=self.detector.vad_mode)
        self.vad_scale = ttk.Scale(self, from_=0, to=3, variable=self.vad_mode, orient=tk.HORIZONTAL, length=150, command=self.update_vad_mode)
        self.vad_scale.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        self.vad_mode_label = ttk.Label(self, text="0 (덜 민감함)", style='Status.TLabel')
        self.vad_mode_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 감지 모드 설정
        detection_frame = ttk.LabelFrame(self, text="감지 방식 선택")
        detection_frame.grid(row=1, column=3, rowspan=2, sticky=tk.NW, padx=5, pady=2)
        
        # RMS 사용 여부 체크박스
        self.rms_check = ttk.Checkbutton(detection_frame, text="RMS 분석 사용", variable=self.app.use_rms, 
                                         command=self.update_detection_mode)
        self.rms_check.pack(anchor=tk.W)
        
        # 주파수 분석 사용 여부 체크박스
        self.freq_check = ttk.Checkbutton(detection_frame, text="주파수 분석 사용", variable=self.app.use_freq,
                                        command=self.update_detection_mode)
        self.freq_check.pack(anchor=tk.W)
        
        # 감지 모드 정보
        ttk.Label(detection_frame, text="참고: VAD는 항상 기본으로 사용됩니다", 
                  font=(self.app.font_family, 8, 'italic')).pack(anchor=tk.W, pady=(5, 0))
        
        # RMS 임계값 설정
        ttk.Label(self, text="음성 감지 임계값:", style='Status.TLabel').grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.voice_threshold = tk.DoubleVar(value=self.detector.VOICE_THRESHOLD)
        self.threshold_scale = ttk.Scale(self, from_=50, to=1000, variable=self.voice_threshold, orient=tk.HORIZONTAL, length=150, command=self.update_voice_threshold)
        self.threshold_scale.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        self.threshold_label = ttk.Label(self, text=f"{self.detector.VOICE_THRESHOLD:.1f}", style='Status.TLabel')
        self.threshold_label.grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        
        # RMS 관련 위젯 저장 (활성화/비활성화를 위해)
        self.rms_widgets = [self.threshold_scale, self.threshold_label]
        
        # 스무딩 팩터 설정
        ttk.Label(self, text="스무딩 팩터:", style='Status.TLabel').grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.smoothing_factor = tk.DoubleVar(value=self.detector.smoothing_factor)
        self.smoothing_scale = ttk.Scale(self, from_=0.1, to=0.9, variable=self.smoothing_factor, orient=tk.HORIZONTAL, length=150, command=self.update_smoothing_factor)
        self.smoothing_scale.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        self.smoothing_label = ttk.Label(self, text=f"{self.detector.smoothing_factor:.1f}", style='Status.TLabel')
        self.smoothing_label.grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 연속 프레임 설정
        ttk.Label(self, text="필요 연속 프레임:", style='Status.TLabel').grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.required_frames = tk.IntVar(value=self.detector.required_speech_frames)
        self.frames_scale = ttk.Scale(self, from_=1, to=10, variable=self.required_frames, orient=tk.HORIZONTAL, length=150, command=self.update_required_frames)
        self.frames_scale.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        self.frames_label = ttk.Label(self, text=str(self.detector.required_speech_frames), style='Status.TLabel')
        self.frames_label.grid(row=4, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 초기 상태 설정 (체크박스에 따라 위젯 활성화/비활성화)
        self.update_detection_mode(show_message=False)
    
    def update_vad_mode(self, event=None):
        """VAD 모드 업데이트"""
        mode = int(self.vad_mode.get())
        self.detector.vad_mode = mode
        self.detector.vad.set_mode(mode)
        
        mode_desc = {
            0: "덜 민감함",
            1: "보통",
            2: "더 민감함",
            3: "가장 민감함"
        }
        
        self.vad_mode_label.config(text=f"{mode} ({mode_desc.get(mode, '')})")
    
    def update_voice_threshold(self, event=None):
        """음성 감지 임계값 업데이트"""
        value = self.voice_threshold.get()
        self.detector.VOICE_THRESHOLD = value
        self.threshold_label.config(text=f"{value:.1f}")
    
    def update_smoothing_factor(self, event=None):
        """스무딩 팩터 업데이트"""
        value = self.smoothing_factor.get()
        self.detector.smoothing_factor = value
        self.smoothing_label.config(text=f"{value:.1f}")
    
    def update_required_frames(self, event=None):
        """필요 연속 프레임 업데이트"""
        value = int(self.required_frames.get())
        self.detector.required_speech_frames = value
        self.frames_label.config(text=str(value))
    
    def update_detection_mode(self, show_message=True):
        """음성 감지 모드 업데이트"""
        # UI에서 detector로 설정 적용
        self.detector.use_rms = self.app.use_rms.get()
        self.detector.use_freq = self.app.use_freq.get()
        
        # RMS 관련 UI 활성화/비활성화
        rms_state = tk.NORMAL if self.app.use_rms.get() else tk.DISABLED
        
        # RMS 임계값 슬라이더와 레이블 활성화/비활성화
        for widget in self.rms_widgets:
            widget.config(state=rms_state)
        
        # 주파수 관련 UI 활성화/비활성화
        freq_state = tk.NORMAL if self.app.use_freq.get() else tk.DISABLED
        
        # 주파수 슬라이더와 레이블 활성화/비활성화
        for widget in self.app.freq_frame.freq_widgets:
            widget.config(state=freq_state)
        
        if show_message:
            # 상태 표시 업데이트
            detection_components = []
            detection_components.append("VAD")  # VAD는 항상 사용
            
            if self.detector.use_rms:
                detection_components.append("RMS")
            
            if self.detector.use_freq:
                detection_components.append("주파수")
            
            detection_mode = " + ".join(detection_components)
            messagebox.showinfo("감지 모드 변경", f"음성 감지 모드가 '{detection_mode}'로 변경되었습니다.")
            
            # 모드 체크 - 최소한 VAD와 하나 이상의 분석 방식 필요
            if not (self.detector.use_rms or self.detector.use_freq):
                messagebox.showwarning("경고", "최소한 RMS 또는 주파수 분석 중 하나는 활성화되어야 합니다.\n"
                                      "그렇지 않으면 VAD만으로는 정확한 음성 감지가 어렵습니다.")