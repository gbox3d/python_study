import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np

class ControlFrame(ttk.Frame):
    """마이크 제어 및 캘리브레이션 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, style='Green.TFrame', padding=10)
        self.app = app
        
        # 마이크 제어 버튼
        self.mic_button = ttk.Button(self, text="마이크 켜기", command=self.app.toggle_microphone)
        self.mic_button.pack(side=tk.LEFT, padx=5)
        
        # 캘리브레이션 시간 설정
        calib_frame = ttk.Frame(self)
        calib_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(calib_frame, text="캘리브레이션 시간(초):").pack(side=tk.LEFT)
        self.calib_time = tk.IntVar(value=10)
        calib_spin = ttk.Spinbox(calib_frame, from_=3, to=30, textvariable=self.calib_time, width=3)
        calib_spin.pack(side=tk.LEFT, padx=2)
        
        # 캘리브레이션 버튼
        self.calibrate_button = ttk.Button(self, text="환경 소음 캘리브레이션", command=self.calibrate)
        self.calibrate_button.pack(side=tk.LEFT, padx=5)
        self.calibrate_button.config(state=tk.DISABLED)
        
        # 캘리브레이션 진행 상태
        self.calib_progress_label = ttk.Label(self, text="")
        self.calib_progress_label.pack(side=tk.LEFT, padx=5)
        
        # 현재 상태 표시
        status_frame = ttk.Frame(self)
        status_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(status_frame, text="상태:", style='Status.TLabel').pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, text="비활성", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # 캘리브레이션 정보
        info_button = ttk.Button(status_frame, text="ℹ️", width=2, 
                                 command=lambda: messagebox.showinfo("캘리브레이션 정보", 
                                                                    "캘리브레이션은 주변 환경 소음을 측정하여 음성 감지 임계값을 자동 조정합니다.\n\n"
                                                                    "권장 사항:\n"
                                                                    "• 조용한 환경: 5-10초\n"
                                                                    "• 약간의 배경 소음: 10-15초\n"
                                                                    "• 시끄러운 환경: 15-30초\n\n"
                                                                    "측정 중에는 정확한 결과를 위해 가능한 조용히 해주세요."))
        info_button.pack(side=tk.LEFT, padx=2)
    
    def update_mic_state(self, is_active):
        """마이크 상태 업데이트"""
        if is_active:
            self.mic_button.config(text="마이크 끄기")
            self.status_label.config(text="활성")
            self.calibrate_button.config(state=tk.NORMAL)
        else:
            self.mic_button.config(text="마이크 켜기")
            self.status_label.config(text="비활성")
            self.calibrate_button.config(state=tk.DISABLED)
    
    def calibrate(self):
        """환경 소음 캘리브레이션"""
        if self.app.running:
            # 시간 확인 (3초 미만이면 경고)
            if self.calib_time.get() < 3:
                messagebox.showwarning("경고", "캘리브레이션 시간은 최소 3초 이상이어야 합니다.")
                self.calib_time.set(3)
                return
                
            # 일시적으로 UI 비활성화
            self.calibrate_button.config(state=tk.DISABLED)
            self.mic_button.config(state=tk.DISABLED)
            
            # 캘리브레이션 스레드 시작
            calib_thread = threading.Thread(target=self.do_calibration, daemon=True)
            calib_thread.start()
    
    def do_calibration(self):
        """백그라운드에서 캘리브레이션 실행"""
        try:
            # 설정된 시간(초) 가져오기
            calib_seconds = self.calib_time.get()
            
            # UI 초기화
            self.app.window.after(0, lambda: self.calib_progress_label.config(text=f"진행 중: {calib_seconds}초 남음"))
            
            # 샘플 수집
            samples = []
            detector = self.app.detector
            chunk_duration = detector.CHUNK / detector.RATE  # 한 청크당 시간(초)
            total_chunks = int(calib_seconds / chunk_duration)
            
            for i in range(total_chunks):
                if not self.app.running:  # 중간에 마이크가 꺼진 경우
                    raise Exception("마이크가 비활성화되었습니다")
                
                # 남은 시간 계산 및 표시
                remaining = calib_seconds - (i * chunk_duration)
                self.app.window.after(0, lambda r=remaining: self.calib_progress_label.config(text=f"진행 중: {r:.1f}초 남음"))
                
                # 오디오 데이터 읽기
                audio_data = detector.stream.read(detector.CHUNK, exception_on_overflow=False)
                rms = detector.get_rms(audio_data)
                samples.append(rms)
                
                # 약간의 지연을 줘서 UI 업데이트 처리
                time.sleep(0.01)
            
            # 배경 소음 레벨 계산 (하위 80%의 평균 사용)
            samples.sort()
            valid_samples = samples[:int(len(samples) * 0.8)]  # 상위 20% 제외 (일시적 소음 제거)
            background_noise = np.mean(valid_samples)
            noise_std = np.std(valid_samples)
            
            # 임계값 설정 (배경 소음 + 표준편차의 4배)
            detector.VOICE_THRESHOLD = background_noise + noise_std * 4.0
            
            # UI 업데이트
            self.app.window.after(0, self.update_after_calibration)
            
        except Exception as e:
            self.app.window.after(0, lambda: messagebox.showerror("오류", f"캘리브레이션 중 오류 발생: {str(e)}"))
            self.app.window.after(0, lambda: self.calibrate_button.config(state=tk.NORMAL))
            self.app.window.after(0, lambda: self.mic_button.config(state=tk.NORMAL))
            self.app.window.after(0, lambda: self.calib_progress_label.config(text=""))
    
    def update_after_calibration(self):
        """캘리브레이션 후 UI 업데이트"""
        detector = self.app.detector
        
        # 파라미터 프레임 업데이트
        self.app.param_frame.voice_threshold.set(detector.VOICE_THRESHOLD)
        self.app.param_frame.threshold_label.config(text=f"{detector.VOICE_THRESHOLD:.1f}")
        
        # 캘리브레이션 버튼 정상화
        self.calibrate_button.config(state=tk.NORMAL)
        self.mic_button.config(state=tk.NORMAL)
        self.calib_progress_label.config(text="완료!")
        
        messagebox.showinfo("완료", f"환경 소음 캘리브레이션이 완료되었습니다.\n새 임계값: {detector.VOICE_THRESHOLD:.1f}")
        
        # 3초 후 완료 텍스트 제거
        self.app.window.after(3000, lambda: self.calib_progress_label.config(text=""))