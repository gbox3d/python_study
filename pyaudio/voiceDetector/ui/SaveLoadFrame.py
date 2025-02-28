import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SaveLoadFrame(ttk.Frame):
    """설정 저장/로드 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, padding=10)
        self.app = app
        
        # 설정 저장/로드 버튼 프레임
        self.save_button = ttk.Button(self, text="설정 저장", command=self.on_save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = ttk.Button(self, text="설정 불러오기", command=self.on_load_settings)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # 기본 설정 버튼 추가
        self.default_button = ttk.Button(self, text="기본 설정 로드", command=self.load_default_settings)
        self.default_button.pack(side=tk.LEFT, padx=5)
        
        # 설정 정보 표시 레이블
        self.settings_info_label = ttk.Label(self, text="", style='Status.TLabel')
        self.settings_info_label.pack(side=tk.RIGHT, padx=5)
    
    def on_save_settings(self):
        """설정 저장"""
        try:
            # UI 값을 detector에 적용
            detector = self.app.detector
            param_frame = self.app.param_frame
            audio_frame = self.app.audio_frame
            freq_frame = self.app.freq_frame
            
            # VAD 및 감지 설정 적용
            detector.vad_mode = param_frame.vad_mode.get()
            detector.VOICE_THRESHOLD = param_frame.voice_threshold.get()
            detector.required_speech_frames = param_frame.required_frames.get()
            detector.human_freq_low = freq_frame.freq_low.get()
            detector.human_freq_high = freq_frame.freq_high.get()
            detector.smoothing_factor = param_frame.smoothing_factor.get()
            detector.use_rms = self.app.use_rms.get()
            detector.use_freq = self.app.use_freq.get()
            
            # 오디오 설정도 적용 (임시 변수가 있으면)
            if hasattr(self.app, 'temp_audio_format'):
                detector.FORMAT = self.app.temp_audio_format
            if hasattr(self.app, 'temp_audio_channels'):
                detector.CHANNELS = self.app.temp_audio_channels
            if hasattr(self.app, 'temp_audio_rate'):
                detector.RATE = self.app.temp_audio_rate
            if hasattr(self.app, 'temp_audio_chunk'):
                detector.CHUNK = self.app.temp_audio_chunk
            
            # 설정 저장 경로 선택
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON 파일", "*.json"), ("모든 파일", "*.*")],
                title="설정 저장"
            )
            
            if not file_path:  # 취소 누른 경우
                return
                
            # 파일에 저장
            if detector.save_settings(file_path):
                messagebox.showinfo("성공", f"설정이 '{file_path}'에 저장되었습니다.")
                self.settings_info_label.config(text="설정 저장됨", foreground="green")
                # 3초 후 메시지 제거
                self.app.window.after(3000, lambda: self.settings_info_label.config(text=""))
            else:
                messagebox.showerror("오류", "설정 저장 실패")
                
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 중 오류 발생: {str(e)}")

    def on_load_settings(self):
        """설정 불러오기"""
        try:
            # 설정 파일 선택
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON 파일", "*.json"), ("모든 파일", "*.*")],
                title="설정 불러오기"
            )
            
            if not file_path:  # 취소 누른 경우
                return
            
            # 마이크가 켜져 있으면 확인
            if self.app.running:
                if not messagebox.askyesno("확인", "마이크가 활성화된 상태에서 설정을 변경하면 재연결됩니다. 계속하시겠습니까?"):
                    return
                
                # 마이크 끄기
                self.app.toggle_microphone()
                
            # 설정 불러오기
            if not self.app.detector.load_settings(file_path):
                messagebox.showerror("오류", f"'{file_path}'에서 설정을 불러올 수 없습니다.")
                return
                
            # UI에 설정 반영
            self.update_all_frames()
            
            # 마이크 다시 켜기 (사용자가 원할 경우)
            if messagebox.askyesno("마이크 켜기", "마이크를 다시 켜시겠습니까?"):
                self.app.toggle_microphone()
            
            messagebox.showinfo("성공", "설정을 성공적으로 불러왔습니다.")
            self.settings_info_label.config(text="설정 로드됨", foreground="green")
            # 3초 후 메시지 제거
            self.app.window.after(3000, lambda: self.settings_info_label.config(text=""))
            
        except Exception as e:
            messagebox.showerror("오류", f"설정 불러오기 중 오류 발생: {str(e)}")
    
    def load_default_settings(self):
        """기본(디폴트) 설정 로드"""
        try:
            # 확인 메시지 표시
            if not messagebox.askyesno("확인", "모든 설정을 기본값으로 초기화하시겠습니까?"):
                return
            
            # 마이크가 켜져 있으면 중지
            was_running = self.app.running
            if was_running:
                self.app.toggle_microphone()
            
            # VoiceDetector의 기본 설정 가져오기
            self.app.detector.reset_to_defaults()
            
            # UI에 설정 반영
            self.update_all_frames()
            
            # 그래프 버퍼 크기 업데이트
            self.app.graph_frame.reset_buffer()
            
            # 정보 메시지 표시
            self.settings_info_label.config(text="기본 설정이 로드되었습니다", foreground="green")
            # 3초 후 메시지 제거
            self.app.window.after(3000, lambda: self.settings_info_label.config(text=""))
            
            # 마이크 재시작 여부 묻기
            if was_running:
                if messagebox.askyesno("마이크 켜기", "마이크를 다시 켜시겠습니까?"):
                    self.app.toggle_microphone()
            
            messagebox.showinfo("완료", "기본 설정이 성공적으로 로드되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"기본 설정 로드 중 오류 발생: {str(e)}")
    
    def update_all_frames(self):
        """모든 프레임에 설정값 반영"""
        detector = self.app.detector
        default_settings = detector.get_current_settings()
        
        # 파라미터 프레임 업데이트
        param_frame = self.app.param_frame
        param_frame.vad_mode.set(default_settings["vad_mode"])
        param_frame.voice_threshold.set(default_settings["voice_threshold"])
        param_frame.required_frames.set(default_settings["required_speech_frames"])
        param_frame.smoothing_factor.set(default_settings["smoothing_factor"])
        
        # 주파수 프레임 업데이트
        freq_frame = self.app.freq_frame
        freq_frame.freq_low.set(default_settings["human_freq_low"])
        freq_frame.freq_high.set(default_settings["human_freq_high"])
        
        # 오디오 프레임 업데이트
        audio_frame = self.app.audio_frame
        audio_frame.audio_format.set(default_settings["format"])
        audio_frame.audio_channels.set(default_settings["channels"])
        audio_frame.audio_rate.set(default_settings["rate"])
        audio_frame.audio_chunk.set(default_settings["chunk"])
        audio_frame.update_chunk_time_label()
        
        # 감지 모드 업데이트
        self.app.use_rms.set(default_settings["use_rms"])
        self.app.use_freq.set(default_settings["use_freq"])
        
        # 라벨 업데이트
        param_frame.update_vad_mode()
        param_frame.threshold_label.config(text=f"{default_settings['voice_threshold']:.1f}")
        param_frame.smoothing_label.config(text=f"{default_settings['smoothing_factor']:.1f}")
        param_frame.frames_label.config(text=str(default_settings['required_speech_frames']))
        freq_frame.freq_low_label.config(text=f"{default_settings['human_freq_low']} Hz")
        freq_frame.freq_high_label.config(text=f"{default_settings['human_freq_high']} Hz")
        
        # 감지 모드 UI 상태 업데이트
        param_frame.update_detection_mode(show_message=False)