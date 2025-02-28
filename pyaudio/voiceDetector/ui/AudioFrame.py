import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio

class AudioFrame(ttk.LabelFrame):
    """오디오 설정 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, text="오디오 설정", padding=10)
        self.app = app
        self.detector = app.detector
        
        # 오디오 형식 설정
        ttk.Label(self, text="오디오 형식:", style='Status.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.audio_format = tk.StringVar()  # 문자열 변수로 변경
        format_combo = ttk.Combobox(self, textvariable=self.audio_format, width=15, state="readonly")

        # 이름과 값 매핑 정의
        self.format_mapping = {
            "16-bit Integer": pyaudio.paInt16,
            "8-bit Integer": pyaudio.paInt8,
            "24-bit Integer": pyaudio.paInt24,
            "32-bit Integer": pyaudio.paInt32,
            "32-bit Float": pyaudio.paFloat32
        }
        # 역방향 매핑 (값 -> 이름)
        self.format_reverse_mapping = {v: k for k, v in self.format_mapping.items()}

        # 콤보박스에 표시될 이름들
        format_combo['values'] = list(self.format_mapping.keys())

        # 현재 값에 해당하는 이름 찾기
        current_format = self.detector.FORMAT
        if current_format in self.format_reverse_mapping:
            self.audio_format.set(self.format_reverse_mapping[current_format])
        else:
            # 기본값 설정
            self.audio_format.set("16-bit Integer")

        format_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        format_combo.bind('<<ComboboxSelected>>', self.update_audio_format)
        
        # 형식 표시 레이블
        self.format_label = ttk.Label(self, text=self.audio_format.get(), style='Status.TLabel')
        self.format_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        
        # 채널 수 설정
        ttk.Label(self, text="채널 수:", style='Status.TLabel').grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        self.audio_channels = tk.IntVar(value=self.detector.CHANNELS)
        channels_combo = ttk.Combobox(self, textvariable=self.audio_channels, width=5, state="readonly")
        channels_combo['values'] = [1, 2]
        channels_combo.current(0 if self.detector.CHANNELS == 1 else 1)
        channels_combo.grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        channels_combo.bind('<<ComboboxSelected>>', self.update_audio_channels)
        
        # 샘플링 레이트 설정
        ttk.Label(self, text="샘플링 레이트 (Hz):", style='Status.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.audio_rate = tk.IntVar(value=self.detector.RATE)
        rate_combo = ttk.Combobox(self, textvariable=self.audio_rate, width=15, state="readonly")
        # VAD 지원 레이트만 표시
        rate_combo['values'] = self.detector.SUPPORTED_VAD_RATES
        # 현재 값에 가장 가까운 인덱스 찾기
        current_rate = self.detector.RATE
        if current_rate in self.detector.SUPPORTED_VAD_RATES:
            rate_combo.current(self.detector.SUPPORTED_VAD_RATES.index(current_rate))
        else:
            rate_combo.current(1)  # 기본값 16000
        rate_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        rate_combo.bind('<<ComboboxSelected>>', self.update_audio_rate)
        
        # 청크 크기 설정
        ttk.Label(self, text="청크 크기 (샘플):", style='Status.TLabel').grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        self.audio_chunk = tk.IntVar(value=self.detector.CHUNK)
        chunk_combo = ttk.Combobox(self, textvariable=self.audio_chunk, width=10, state="readonly")
        # 일반적인 청크 크기 옵션
        chunk_options = [256, 480, 512, 1024, 2048, 4096]
        chunk_combo['values'] = chunk_options
        # 현재 값에 가장 가까운 인덱스 찾기
        current_chunk = self.detector.CHUNK
        if current_chunk in chunk_options:
            chunk_combo.current(chunk_options.index(current_chunk))
        else:
            # 가장 가까운 값 찾기
            closest_index = min(range(len(chunk_options)), key=lambda i: abs(chunk_options[i] - current_chunk))
            chunk_combo.current(closest_index)
        chunk_combo.grid(row=1, column=4, sticky=tk.W, padx=5, pady=2)
        chunk_combo.bind('<<ComboboxSelected>>', self.update_audio_chunk)
        
        # 오디오 설정 적용 버튼
        apply_audio_button = ttk.Button(self, text="오디오 설정 적용", command=self.apply_audio_settings)
        apply_audio_button.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # 오디오 설정 상태 표시
        self.audio_settings_status = ttk.Label(self, text="", style='Status.TLabel')
        self.audio_settings_status.grid(row=2, column=2, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        # 현재 청크 시간 표시
        self.chunk_time_label = ttk.Label(self, text=f"프레임 시간: {self.detector.CHUNK / self.detector.RATE * 1000:.1f} ms", 
                                         font=(self.app.font_family, 8))
        self.chunk_time_label.grid(row=3, column=0, columnspan=5, sticky=tk.W, padx=5)
        
        # 컴보박스 참조 저장
        self.format_combo = format_combo
        self.channels_combo = channels_combo
        self.rate_combo = rate_combo
        self.chunk_combo = chunk_combo
    
    def update_audio_format(self, event=None):
        selected_format_name = self.audio_format.get()
        # 이름으로부터 실제 pyaudio 값 가져오기
        selected_format_value = self.format_mapping[selected_format_name]
        
        # detector의 FORMAT 값 업데이트
        self.detector.FORMAT = selected_format_value
        
        # 형식 레이블 업데이트
        self.format_label.config(text=selected_format_name)
        
        # 필요한 경우 관련 설정 업데이트
        # ...
        
        # 로그 또는 상태 메시지 (옵션)
        print(f"오디오 형식이 {selected_format_name}으로 변경되었습니다.")
    
    def update_audio_channels(self, event=None):
        """오디오 채널 수 업데이트"""
        # 콤보박스에서 선택된 값 가져오기
        selected = self.audio_channels.get()
        # 설정값 임시 저장
        self.app.temp_audio_channels = selected
    
    def update_audio_rate(self, event=None):
        """오디오 샘플링 레이트 업데이트"""
        # 콤보박스에서 선택된 값 가져오기
        selected = self.audio_rate.get()
        # 설정값 임시 저장
        self.app.temp_audio_rate = selected
        # 청크 시간 업데이트
        self.update_chunk_time_label()
    
    def update_audio_chunk(self, event=None):
        """오디오 청크 크기 업데이트"""
        # 콤보박스에서 선택된 값 가져오기
        selected = self.audio_chunk.get()
        # 설정값 임시 저장
        self.app.temp_audio_chunk = selected
        # 청크 시간 업데이트
        self.update_chunk_time_label()
    
    def update_chunk_time_label(self):
        """청크 시간 레이블 업데이트"""
        # 임시 저장된 값이 있으면 사용, 없으면 현재 detector 값 사용
        chunk = getattr(self.app, 'temp_audio_chunk', self.detector.CHUNK)
        rate = getattr(self.app, 'temp_audio_rate', self.detector.RATE)
        # 밀리초 단위로 계산
        time_ms = chunk / rate * 1000
        self.chunk_time_label.config(text=f"프레임 시간: {time_ms:.1f} ms")
    
    def apply_audio_settings(self):
        """임시 저장된 오디오 설정을 적용"""
        # 마이크가 활성화된 상태인지 확인
        if self.app.running:
            if not messagebox.askyesno("확인", "마이크가 활성화된 상태에서 오디오 설정을 변경하면 재연결됩니다. 계속하시겠습니까?"):
                return
        
        try:
            # 임시 저장된 설정값 가져오기
            settings = {}
            
            if hasattr(self.app, 'temp_audio_format'):
                settings['format'] = self.app.temp_audio_format
            
            if hasattr(self.app, 'temp_audio_channels'):
                settings['channels'] = self.app.temp_audio_channels
            
            if hasattr(self.app, 'temp_audio_rate'):
                settings['rate'] = self.app.temp_audio_rate
            
            if hasattr(self.app, 'temp_audio_chunk'):
                settings['chunk'] = self.app.temp_audio_chunk
            
            # 설정값이 비어있으면 무시
            if not settings:
                self.audio_settings_status.config(text="변경된 설정 없음", foreground="blue")
                return
            
            # 마이크 상태 저장
            was_running = self.app.running
            
            # 마이크가 켜져 있으면 일시 중지
            if was_running:
                self.app.toggle_microphone()
            
            # 설정 적용
            changed = self.detector.apply_settings(settings)
            
            # 마이크 다시 시작
            if was_running:
                self.app.toggle_microphone()
            
            # 상태 메시지 표시
            if changed:
                self.audio_settings_status.config(text="설정이 성공적으로 적용되었습니다", foreground="green")
                
                # 현재 오디오 설정 정보 가져오기
                settings_info = self.detector.get_audio_settings_summary()
                info_text = f"형식: {settings_info['format']}, 채널: {settings_info['channels']}, " \
                           f"샘플링: {settings_info['rate']}, 청크: {settings_info['chunk']}"
                
                messagebox.showinfo("오디오 설정 변경", f"오디오 설정이 변경되었습니다.\n\n{info_text}")
                
                # 임시 변수 초기화
                if hasattr(self.app, 'temp_audio_format'):
                    delattr(self.app, 'temp_audio_format')
                if hasattr(self.app, 'temp_audio_channels'):
                    delattr(self.app, 'temp_audio_channels')
                if hasattr(self.app, 'temp_audio_rate'):
                    delattr(self.app, 'temp_audio_rate')
                if hasattr(self.app, 'temp_audio_chunk'):
                    delattr(self.app, 'temp_audio_chunk')
                
                # 그래프 데이터 초기화
                self.update_chunk_time_label()
                
                # 설정된 값 UI에 업데이트
                self.update_ui_values()
                
                # 그래프 버퍼 크기 조정 (새 청크 크기에 맞춤)
                self.app.graph_frame.reset_buffer()
            else:
                self.audio_settings_status.config(text="변경사항 없음", foreground="blue")
            
            # 일정 시간 후 상태 메시지 지우기
            self.app.window.after(3000, lambda: self.audio_settings_status.config(text=""))
            
        except Exception as e:
            self.audio_settings_status.config(text="오류 발생", foreground="red")
            messagebox.showerror("오류", f"오디오 설정 적용 중 오류 발생: {str(e)}")
    
    
    def update_ui_values(self):
        """현재 detector 값으로 UI 업데이트"""
        # 현재 FORMAT 값에 맞는 이름을 찾아 설정
        format_name = self.format_reverse_mapping.get(self.detector.FORMAT, "Unknown")
        self.audio_format.set(format_name)
        
        # 형식 레이블 업데이트
        if hasattr(self, 'format_info'):
            # 상세 정보가 있는 경우
            self.format_label.config(text=self.format_info.get(format_name, "Unknown"))
        else:
            # 일반 레이블만 있는 경우
            self.format_label.config(text=format_name)
        
        # 나머지 값들 업데이트
        self.audio_channels.set(self.detector.CHANNELS)
        self.audio_rate.set(self.detector.RATE)
        self.audio_chunk.set(self.detector.CHUNK)
        self.update_chunk_time_label()