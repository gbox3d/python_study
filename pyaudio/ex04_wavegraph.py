import pygame
import numpy as np
import struct
import threading
import time
import sys

# pyaudio 직접 사용
import pyaudio
from scipy.fftpack import fft

class SimpleWaveformVisualizer:
    def __init__(self, width=1200, height=400):
        # Pygame 초기화
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("단순 오디오 파형 시각화")
        
        # 폰트 설정
        # 폰트 파일 경로 (현재 디렉토리 기준)
        font_path = "./DungGeunMo.ttf"
        try:
            self.font = pygame.font.Font(font_path, 24)
            print("폰트 로딩 성공")
        except:
            print("폰트 로딩 실패: 기본 폰트 사용")
            self.font = pygame.font.SysFont(None, 24)
        
        # 색상 설정
        self.bg_color = (10, 10, 20)
        self.grid_color = (40, 40, 50)
        self.wave_color = (0, 255, 100)
        self.text_color = (220, 220, 220)
        
        # 오디오 설정
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024  # 청크 크기 증가 (더 많은 데이터 처리)
        
        # 파형 데이터 버퍼
        self.buffer_size = self.width  # 화면 픽셀 수에 맞춤
        self.audio_buffer = np.zeros(self.buffer_size)
        
        # Y축 스케일
        self.y_scale = 1.0
        self.y_max = 32768
        
        # 상태 변수
        self.running = True
        self.paused = False
        
        # 오디오 스트림 초기화
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        # 오디오 수집 스레드
        self.thread = threading.Thread(target=self.collect_audio, daemon=True)
        
        # 성능 측정
        self.clock = pygame.time.Clock()
        self.fps = 0
        
        # 표시 모드
        self.display_mode = 0  # 0: 파형, 1: FFT
        
        # FFT 데이터
        self.fft_data = np.zeros(self.CHUNK//2)
        
    def collect_audio(self):
        """백그라운드에서 오디오 데이터 수집"""
        while self.running:
            if not self.paused:
                try:
                    # 오디오 데이터 읽기
                    audio_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                    
                    # 오디오 데이터를 short 배열로 변환
                    count = len(audio_data) // 2
                    format_str = "%dh" % count
                    shorts = struct.unpack(format_str, audio_data)
                    
                    # 파형 데이터 버퍼 업데이트
                    self.audio_buffer = np.roll(self.audio_buffer, -len(shorts))
                    self.audio_buffer[-len(shorts):] = shorts
                    
                    # FFT 계산 (주파수 스펙트럼)
                    if self.display_mode == 1:
                        fft_data = fft(shorts)
                        # 절반만 사용 (나머지는 대칭)
                        self.fft_data = np.abs(fft_data[:len(fft_data)//2])
                        
                except Exception as e:
                    print(f"오디오 데이터 수집 오류: {e}")
            
            # 잠깐 쉬기
            time.sleep(0.01)
    
    def draw_waveform(self):
        """파형 그리기"""
        # 화면 지우기
        self.screen.fill(self.bg_color)
        
        # 그리드 그리기
        self.draw_grid()
        
        if self.display_mode == 0:
            # 시간 도메인 파형 그리기
            center_y = self.height // 2
            
            # 포인트 수집 (최적화)
            points = []
            # 화면 픽셀 하나당 하나의 데이터 포인트를 표시 (더 빠른 렌더링)
            step = max(1, len(self.audio_buffer) // self.width)
            for i in range(0, len(self.audio_buffer), step):
                x = int(i * self.width / len(self.audio_buffer))
                
                # Y축 스케일 적용 및 값 제한
                value = self.audio_buffer[i] * self.y_scale
                clamped_value = max(min(value, self.y_max), -self.y_max)
                y = center_y - int(clamped_value * center_y / self.y_max)
                
                points.append((x, y))
            
            # 파형 그리기
            if len(points) > 1:
                pygame.draw.lines(self.screen, self.wave_color, False, points, 2)
        
        elif self.display_mode == 1:
            # 주파수 도메인 (FFT) 그리기
            if len(self.fft_data) > 0:
                bar_width = max(1, self.width // len(self.fft_data))
                for i in range(len(self.fft_data)):
                    # 진폭 계산 (로그 스케일)
                    amplitude = self.fft_data[i]
                    # 정규화 및 스케일 적용
                    scaled_height = np.log10(1 + amplitude) * self.y_scale * 20
                    # 높이 제한
                    height = min(int(scaled_height), self.height)
                    
                    # 막대 그리기
                    x = i * bar_width
                    pygame.draw.rect(
                        self.screen, 
                        self.wave_color, 
                        (x, self.height - height, bar_width, height)
                    )
        
        # 정보 표시
        self.draw_info()
        
        # 화면 업데이트
        pygame.display.flip()
    
    def draw_grid(self):
        """배경 그리드 그리기"""
        # 수평선 (25% 간격)
        for i in range(1, 4):
            y = int(self.height * i / 4)
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y), 1)
        
        # 수직선 (25% 간격)
        for i in range(1, 4):
            x = int(self.width * i / 4)
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height), 1)
        
        # 중앙선 (파형 모드에서만)
        if self.display_mode == 0:
            center_y = self.height // 2
            pygame.draw.line(self.screen, (100, 100, 120), (0, center_y), (self.width, center_y), 2)
    
    def draw_info(self):
        """정보 텍스트 표시"""
        # FPS 표시
        fps_text = self.font.render(f"FPS: {self.fps}", True, self.text_color)
        self.screen.blit(fps_text, (10, 10))
        
        # 현재 모드 표시
        mode_name = "파형" if self.display_mode == 0 else "주파수 스펙트럼"
        mode_text = self.font.render(f"모드: {mode_name} (M 키로 전환)", True, self.text_color)
        self.screen.blit(mode_text, (10, 40))
        
        # Y 스케일 표시
        scale_text = self.font.render(f"스케일: {self.y_scale:.2f} (↑/↓ 키로 조절)", True, self.text_color)
        self.screen.blit(scale_text, (10, 70))
        
        # 상태 표시
        status = "일시정지" if self.paused else "재생 중"
        status_text = self.font.render(f"상태: {status} (스페이스바)", True, self.text_color)
        self.screen.blit(status_text, (10, 100))
        
        # 종료 안내
        exit_text = self.font.render("종료: ESC 키", True, self.text_color)
        self.screen.blit(exit_text, (10, 130))
    
    def handle_events(self):
        """사용자 입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # ESC 키: 종료
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # 스페이스바: 일시정지/재생
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                
                # M 키: 모드 전환
                elif event.key == pygame.K_m:
                    self.display_mode = (self.display_mode + 1) % 2
                
                # 위쪽 화살표: Y 스케일 증가
                elif event.key == pygame.K_UP:
                    self.y_scale *= 1.2
                
                # 아래쪽 화살표: Y 스케일 감소
                elif event.key == pygame.K_DOWN:
                    self.y_scale /= 1.2
                    if self.y_scale < 0.01:
                        self.y_scale = 0.01
    
    def run(self):
        """메인 루프"""
        try:
            # 오디오 수집 스레드 시작
            self.thread.start()
            
            # 메인 루프
            while self.running:
                # 이벤트 처리
                self.handle_events()
                
                # 파형 그리기
                self.draw_waveform()
                
                # FPS 계산 및 제한
                self.fps = int(self.clock.get_fps())
                self.clock.tick(60)  # 최대 60 FPS
                
        finally:
            # 종료 전 정리
            self.cleanup()
    
    def cleanup(self):
        """리소스 정리"""
        # 스레드 종료 대기
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        
        # 오디오 스트림 종료
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
        
        if self.p:
            self.p.terminate()
        
        # Pygame 종료
        pygame.quit()
        print("프로그램 종료")


if __name__ == "__main__":
    # 명령줄 인자로 크기 지정 가능
    width = 1200
    height = 400
    
    if len(sys.argv) >= 3:
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
        except:
            pass
    
    # 시각화기 실행
    visualizer = SimpleWaveformVisualizer(width, height)
    visualizer.run()