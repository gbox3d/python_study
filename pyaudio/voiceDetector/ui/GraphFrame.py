import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import collections
import struct
import numpy as np

class GraphFrame(ttk.Frame):
    """오디오 시각화 그래프 프레임"""
    
    def __init__(self, parent, app):
        """프레임 초기화"""
        super().__init__(parent, padding=10)
        self.app = app
        self.detector = app.detector
        
        # 그래프 초기화
        self.setup_audio_graph()
        
    def setup_audio_graph(self):
        """오디오 시각화 그래프 초기화"""
        try:
            # 그래프 제어 프레임 추가
            graph_control_frame = ttk.Frame(self)
            graph_control_frame.pack(fill=tk.X, pady=(0, 5))
            
            # Y축 스케일 선택 콤보박스
            scale_frame = ttk.Frame(graph_control_frame)
            scale_frame.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(scale_frame, text="Y축 스케일:", style='Status.TLabel').pack(side=tk.LEFT, padx=2)
            
            self.y_scale_var = tk.StringVar()
            y_scale_combo = ttk.Combobox(scale_frame, textvariable=self.y_scale_var, width=15, state="readonly")
            y_scale_combo['values'] = ("±32768 (16비트)", "±16384", "±8192", "±4096", "±2048", "±1024", "±512", "자동")
            y_scale_combo.current(0)  # 기본값 설정
            y_scale_combo.pack(side=tk.LEFT, padx=2)
            y_scale_combo.bind('<<ComboboxSelected>>', self.update_y_scale)
            
            # 사용자 정의 Y축 범위 설정
            custom_frame = ttk.Frame(graph_control_frame)
            custom_frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(custom_frame, text="최소:", style='Status.TLabel').pack(side=tk.LEFT, padx=2)
            self.y_min_var = tk.IntVar(value=-32768)
            y_min_entry = ttk.Entry(custom_frame, textvariable=self.y_min_var, width=8)
            y_min_entry.pack(side=tk.LEFT, padx=2)
            
            ttk.Label(custom_frame, text="최대:", style='Status.TLabel').pack(side=tk.LEFT, padx=2)
            self.y_max_var = tk.IntVar(value=32768)
            y_max_entry = ttk.Entry(custom_frame, textvariable=self.y_max_var, width=8)
            y_max_entry.pack(side=tk.LEFT, padx=2)
            
            apply_button = ttk.Button(custom_frame, text="적용", command=self.apply_custom_scale, width=5)
            apply_button.pack(side=tk.LEFT, padx=2)
            
            # 자동 스케일 갱신 주기
            auto_frame = ttk.Frame(graph_control_frame)
            auto_frame.pack(side=tk.RIGHT, padx=5)
            
            self.auto_scale = tk.BooleanVar(value=False)
            auto_check = ttk.Checkbutton(auto_frame, text="자동 스케일 갱신", variable=self.auto_scale)
            auto_check.pack(side=tk.LEFT, padx=2)
            
            # matplotlib 그래프 설정
            self.fig, self.ax = plt.subplots(figsize=(6, 2), dpi=100)
            self.fig.patch.set_facecolor('#f0f0f0')  # 배경색 설정
            
            # 버퍼 크기 설정
            self.reset_buffer()
            
            # 플롯 생성 및 스타일 설정
            self.line, = self.ax.plot(range(len(self.audio_data_buffer)), self.audio_data_buffer, 
                                    lw=1, color='blue')
            
            # 축 설정
            self.ax.set_ylim(-32768, 32768)  # 16비트 오디오의 범위
            self.ax.set_xlim(0, len(self.audio_data_buffer))
            self.ax.set_title('실시간 오디오 파형')
            self.ax.set_xlabel('샘플')
            self.ax.set_ylabel('진폭')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # 여백 조정
            self.fig.tight_layout()
            
            # 캔버스에 그래프 추가
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 카운터 변수 초기화
            self.scale_counter = 0
            
        except Exception as e:
            messagebox.showerror("그래프 초기화 오류", f"그래프 초기화 중 오류 발생: {str(e)}")
            # 오류 발생 시 그래프 없이 계속 진행
            pass
    
    def reset_buffer(self):
        """버퍼 초기화"""
        # 버퍼 크기 계산 - 100프레임 저장
        self.buffer_size = 100 * (self.detector.CHUNK // 2)
        # 빈 데이터로 초기화
        self.audio_data_buffer = collections.deque([0] * self.buffer_size, maxlen=self.buffer_size)
        
        # 그래프가 이미 존재하면 X축 범위 업데이트
        if hasattr(self, 'ax') and self.ax is not None:
            self.ax.set_xlim(0, self.buffer_size)
            if hasattr(self, 'canvas') and self.canvas is not None:
                self.canvas.draw_idle()
    
    def update_y_scale(self, event=None):
        """Y축 스케일 업데이트 (콤보박스 선택)"""
        if self.app.is_closing:
            return
            
        selected = self.y_scale_var.get()
        
        # 선택된 옵션에 따라 Y축 범위 설정
        if selected == "±32768 (16비트)":
            y_min, y_max = -32768, 32768
        elif selected == "±16384":
            y_min, y_max = -16384, 16384
        elif selected == "±8192":
            y_min, y_max = -8192, 8192
        elif selected == "±4096":
            y_min, y_max = -4096, 4096
        elif selected == "±2048":
            y_min, y_max = -2048, 2048
        elif selected == "±1024":
            y_min, y_max = -1024, 1024
        elif selected == "±512":
            y_min, y_max = -512, 512
        elif selected == "자동":
            # 현재 데이터 기반 자동 스케일링
            data = list(self.audio_data_buffer)
            if data:
                margin = (max(data) - min(data)) * 0.1  # 10% 여유 공간
                y_min, y_max = min(data) - margin, max(data) + margin
            else:
                y_min, y_max = -1000, 1000
        
        # 엔트리 위젯 업데이트
        self.y_min_var.set(y_min)
        self.y_max_var.set(y_max)
        
        # 그래프 Y축 업데이트
        self.ax.set_ylim(y_min, y_max)
        self.canvas.draw_idle()
        print(f"Y축 스케일 변경: {y_min} ~ {y_max}")

    def apply_custom_scale(self):
        """사용자 정의 Y축 범위 적용"""
        if self.app.is_closing:
            return
            
        try:
            y_min = self.y_min_var.get()
            y_max = self.y_max_var.get()
            
            # 유효성 검사
            if y_min >= y_max:
                messagebox.showerror("오류", "최소값은 최대값보다 작아야 합니다.")
                return
                
            # 그래프 Y축 업데이트
            self.ax.set_ylim(y_min, y_max)
            self.canvas.draw_idle()
            
            # 콤보박스 선택 해제 (사용자 정의 상태)
            self.y_scale_var.set("")
            print(f"사용자 정의 Y축 적용: {y_min} ~ {y_max}")
            
        except Exception as e:
            messagebox.showerror("오류", f"Y축 범위 설정 오류: {str(e)}")
    
    def update_graph(self, audio_data):
        """그래프 데이터 업데이트 - 스크롤 효과 적용"""
        # 애플리케이션이 종료 중이면 업데이트 중단
        if self.app.is_closing:
            return
            
        try:
            # 오디오 데이터를 short 배열로 변환
            count = len(audio_data) // 2
            format_str = "%dh" % count
            shorts = struct.unpack(format_str, audio_data)
            
            # 새 데이터 추가
            self.audio_data_buffer.extend(shorts)
            
            # 매 프레임마다 그래프 업데이트
            if not self.app.is_closing and hasattr(self, 'line') and self.line is not None:
                # 그래프 데이터 업데이트
                data_array = list(self.audio_data_buffer)
                self.line.set_ydata(data_array)
                
                # x축 범위 항상 동일하게 유지 (전체 버퍼 크기)
                self.ax.set_xlim(0, len(data_array))
                
                # 자동 스케일 갱신이 활성화된 경우
                if hasattr(self, 'auto_scale') and self.auto_scale.get():
                    # 10프레임마다 자동 스케일 갱신 (성능 최적화)
                    if not hasattr(self, 'scale_counter'):
                        self.scale_counter = 0
                    self.scale_counter += 1
                    
                    if self.scale_counter % 10 == 0:
                        if data_array:
                            # 데이터 범위 계산
                            data_min = min(data_array)
                            data_max = max(data_array)
                            
                            # 약간의 여유 공간 추가 (10%)
                            margin = (data_max - data_min) * 0.1
                            new_min = data_min - margin
                            new_max = data_max + margin
                            
                            # 일정 최소 범위 보장 (너무 작은 범위 방지)
                            if new_max - new_min < 1000:
                                center = (new_max + new_min) / 2
                                new_min = center - 500
                                new_max = center + 500
                                
                            # Y축 업데이트
                            self.ax.set_ylim(new_min, new_max)
                            
                            # UI 업데이트 (쓰레드 안전하게)
                            if hasattr(self, 'y_min_var'):
                                self.app.window.after(0, lambda: self.y_min_var.set(int(new_min)))
                            if hasattr(self, 'y_max_var'):
                                self.app.window.after(0, lambda: self.y_max_var.set(int(new_max)))
                
                try:
                    # 캔버스 업데이트
                    if hasattr(self, 'canvas') and self.canvas is not None:
                        self.canvas.draw_idle()  # draw_idle은 더 효율적
                except Exception as e:
                    # 이미 파괴된 캔버스 관련 오류 무시
                    pass
                    
        except Exception as e:
            if not self.app.is_closing:
                print(f"그래프 업데이트 오류 (무시됨): {e}")
    
    def cleanup(self):
        """리소스 정리"""
        # matplotlib 리소스 정리
        if hasattr(self, 'canvas') and self.canvas is not None:
            try:
                # 캔버스의 모든 잠재적 idle_draw 콜백 해제 시도
                try:
                    if hasattr(self.canvas, '_idle_draw_id'):
                        self.app.window.after_cancel(self.canvas._idle_draw_id)
                except:
                    pass
                
                # 캔버스 참조 제거
                self.canvas = None
            except Exception as e:
                print(f"캔버스 정리 오류 (무시됨): {e}")
        
        if hasattr(self, 'fig') and self.fig is not None:
            try:
                plt.close(self.fig)
                print("그래프 리소스 정리")
                self.fig = None
                self.ax = None
                self.line = None
            except Exception as e:
                print(f"그래프 정리 오류 (무시됨): {e}")