import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os

# UI 프레임 임포트
from ui.ControlFrame import ControlFrame
from ui.StatusFrame import StatusFrame
from ui.ParamFrame import ParamFrame
from ui.AudioFrame import AudioFrame
from ui.FreqFrame import FreqFrame 
from ui.GraphFrame import GraphFrame

# 유틸리티 임포트
from utils.FontManager import FontManager

# VoiceDetector 클래스 임포트
from VoiceDetector import VoiceDetector


class VoiceDetectorApp:
    """음성 감지기 모니터링 애플리케이션 메인 클래스"""
    
    def __init__(self):
        """애플리케이션 초기화"""
        # 윈도우 초기화
        self.window = tk.Tk()
        self.window.title("Voice Detector Monitor")
        self.window.geometry("650x700+50+50")  # 윈도우 크기 설정
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 애플리케이션 상태 플래그
        self.is_closing = False
        self.running = False
        self.thread = None
        
        # 폰트 설정
        self.font_manager = FontManager()
        self.normal_font = self.font_manager.normal_font
        self.header_font = self.font_manager.header_font
        self.title_font = self.font_manager.title_font
        self.font_family = self.font_manager.font_family
        
        # VoiceDetector 초기화
        self.detector = VoiceDetector(debug_mode=False)
        
        # 감지 모드 변수 초기화 (detector의 값으로)
        self.use_rms = tk.BooleanVar(value=self.detector.use_rms)
        self.use_freq = tk.BooleanVar(value=self.detector.use_freq)
        
        # 스타일 설정
        self.setup_styles()
        
        # 스크롤 가능한 메인 프레임 생성
        self.main_canvas, self.main_frame = self.create_scrollable_frame()
        
        # 제목 추가
        title_label = ttk.Label(self.main_frame, text="음성 감지기 모니터링", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # UI 컴포넌트 초기화
        self.init_ui_components()
        
    def setup_styles(self):
        """UI 스타일 설정"""
        self.style = ttk.Style()
        self.style.configure('Green.TFrame', background='#E8F5E9')
        self.style.configure('LightBlue.TFrame', background='#E3F2FD')
        self.style.configure('Status.TLabel', font=self.normal_font)
        self.style.configure('Header.TLabel', font=self.header_font)
        self.style.configure('Title.TLabel', font=self.title_font)
        
    def create_scrollable_frame(self):
        """스크롤 가능한 메인 프레임 생성"""
        # 1. 캔버스 생성
        canvas = tk.Canvas(self.window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 2. 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 3. 내부 프레임 생성 (실제 위젯을 담을 프레임)
        main_frame = ttk.Frame(canvas, padding=10)
        
        # 4. 캔버스 내에 윈도우 생성
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # 캔버스 크기 변경 시 내부 프레임 크기 조정
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_window(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        main_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_window)
        
        # 마우스 휠 스크롤 이벤트 바인딩
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux
        
        return canvas, main_frame
        
    def init_ui_components(self):
        """UI 컴포넌트 초기화"""
        # 컨트롤 프레임 (마이크 켜기/끄기, 캘리브레이션)
        self.control_frame = ControlFrame(self.main_frame, self)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        # 설정 저장/로드 프레임
        from ui.SaveLoadFrame import SaveLoadFrame
        self.save_load_frame = SaveLoadFrame(self.main_frame, self)
        self.save_load_frame.pack(fill=tk.X, pady=5)
        
        # 상태 표시 프레임 (감지 상태 표시)
        self.status_frame = StatusFrame(self.main_frame, self)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        # 주파수 범위 설정 프레임
        self.freq_frame = FreqFrame(self.main_frame, self)
        self.freq_frame.pack(fill=tk.X, pady=5)
        
        # 파라미터 설정 프레임 (VAD 모드, 임계값 등)
        self.param_frame = ParamFrame(self.main_frame, self)
        self.param_frame.pack(fill=tk.X, pady=5)
        
        # 오디오 설정 프레임
        self.audio_frame = AudioFrame(self.main_frame, self)
        self.audio_frame.pack(fill=tk.X, pady=5)
        
        
        
        # 그래프 프레임
        self.graph_frame = GraphFrame(self.main_frame, self)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def update_status(self):
        """주기적으로 음성 감지 상태 업데이트"""
        last_vad = False
        last_rms = 0
        last_freq = False
        last_speech = False
        
        try:
            while self.running and not self.is_closing:
                # 애플리케이션이 종료 중이면 루프 종료
                if self.is_closing:
                    print("업데이트 스레드 종료됨 (애플리케이션 종료 중)")
                    break
                    
                try:
                    # 오디오 데이터 읽기
                    audio_data = self.detector.stream.read(self.detector.CHUNK, exception_on_overflow=False)
                    
                    # 그래프 업데이트
                    self.graph_frame.update_graph(audio_data)
                    
                    # UI와 detector의 설정 동기화
                    self.detector.use_rms = self.use_rms.get()
                    self.detector.use_freq = self.use_freq.get()
                    
                    # VoiceDetector의 detect_speech 메서드 사용하여 음성 감지
                    speech_detected, vad_result, smoothed_rms, rms_result, freq_result = self.detector.detect_speech(audio_data)
                    
                    # 연속 음성 판단
                    is_continuous = self.detector.is_speech_continuous()
                    
                    # 값이 변경되었을 때만 UI 업데이트
                    if vad_result != last_vad or abs(smoothed_rms - last_rms) > 1 or freq_result != last_freq or is_continuous != last_speech:
                        if not self.is_closing:  # 종료 중이 아닐 때만 UI 업데이트
                            self.window.after(0, lambda v=vad_result, r=smoothed_rms, f=freq_result, s=self.detector.consecutive_speech, 
                                            c=is_continuous, sd=speech_detected: self.status_frame.update_ui(v, r, f, s, c, sd))
                        
                        last_vad = vad_result
                        last_rms = smoothed_rms
                        last_freq = freq_result
                        last_speech = is_continuous
                    
                except Exception as e:
                    if not self.is_closing:  # 종료 중이 아닐 때만 오류 출력
                        print(f"오디오 처리 오류 (계속 진행): {e}")
                    time.sleep(0.1)  # 오류 발생 시 잠시 대기
                
                time.sleep(0.05)  # 업데이트 주기 (약 20fps)
                
        except Exception as e:
            if not self.is_closing:  # 종료 중이 아닐 때만 오류 메시지 표시
                print(f"업데이트 스레드 오류: {e}")
                self.window.after(0, lambda: messagebox.showerror("오류", f"음성 감지 업데이트 중 오류 발생: {str(e)}"))
                self.window.after(0, self.toggle_microphone)
        
        print("업데이트 스레드 종료됨")
    
    def toggle_microphone(self):
        """마이크 켜기/끄기 토글"""
        if not self.running:
            # 마이크 켜기
            try:
                # 임시 오디오 설정이 있으면 먼저 적용
                settings = {}
                if hasattr(self, 'temp_audio_format'):
                    settings['format'] = self.temp_audio_format
                if hasattr(self, 'temp_audio_channels'):
                    settings['channels'] = self.temp_audio_channels
                if hasattr(self, 'temp_audio_rate'):
                    settings['rate'] = self.temp_audio_rate
                if hasattr(self, 'temp_audio_chunk'):
                    settings['chunk'] = self.temp_audio_chunk
                
                if settings:
                    self.detector.apply_settings(settings)
                    # 임시 변수 초기화
                    if hasattr(self, 'temp_audio_format'):
                        delattr(self, 'temp_audio_format')
                    if hasattr(self, 'temp_audio_channels'):
                        delattr(self, 'temp_audio_channels')
                    if hasattr(self, 'temp_audio_rate'):
                        delattr(self, 'temp_audio_rate')
                    if hasattr(self, 'temp_audio_chunk'):
                        delattr(self, 'temp_audio_chunk')
                    
                    # 그래프 버퍼 크기 업데이트
                    self.graph_frame.reset_buffer()
                
                # UI에 현재 설정값 표시
                self.audio_frame.update_ui_values()
                
                # 마이크 스트림 초기화
                self.detector.initialize_stream()
                self.running = True
                self.thread = threading.Thread(target=self.update_status, daemon=True)
                self.thread.start()
                
                # 컨트롤 프레임 상태 업데이트
                self.control_frame.update_mic_state(True)
                
            except Exception as e:
                messagebox.showerror("오류", f"마이크를 시작할 수 없습니다: {str(e)}")
        else:
            # 마이크 끄기
            self.running = False
            if self.thread:
                self.thread.join(timeout=1.0)
            self.detector.close_stream()
            
            # 컨트롤 프레임 상태 업데이트
            self.control_frame.update_mic_state(False)
            
            # 상태 프레임 초기화
            self.status_frame.reset_ui()
    
    def on_closing(self):
        """창 닫기 처리"""
        # 종료 중임을 표시
        self.is_closing = True
        print("애플리케이션 종료 중...")
        
        # 잠시 대기하여 UI 업데이트가 완료되도록 함
        self.window.after(100)
        
        # 마이크 및 스레드 정리
        if self.running:
            self.running = False
            print("스레드 종료 중...")
            if self.thread:
                try:
                    # 최대 2초 동안 스레드 종료 대기
                    self.thread.join(timeout=2.0)
                    if self.thread.is_alive():
                        print("경고: 스레드가 완전히 종료되지 않았습니다.")
                except Exception as e:
                    print(f"스레드 종료 오류 (무시됨): {e}")
            
            try:
                self.detector.close_stream()
                print("오디오 스트림 종료")
            except Exception as e:
                print(f"스트림 종료 오류 (무시됨): {e}")
        
        # 그래프 리소스 정리
        self.graph_frame.cleanup()
        
        # 최종 윈도우 정리를 별도의 after 콜백으로 실행
        self.window.after(200, self._final_cleanup)

    def _final_cleanup(self):
        """최종 정리 및 윈도우 종료"""
        try:
            print("최종 정리 및 윈도우 종료")
            self.window.destroy()
        except Exception as e:
            print(f"최종 정리 오류: {e}")
            import sys
            sys.exit(0)  # 강제 종료
            
    def run(self):
        """애플리케이션 실행"""
        self.window.mainloop()