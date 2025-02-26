import pyaudio
import numpy as np
import pygame
import struct

# 오디오 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # 샘플링 레이트
CHUNK = 1024  # 버퍼 크기

# pygame 설정
WIDTH, HEIGHT = 800, 300
BAR_WIDTH = 600
BAR_HEIGHT = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_rms(block):
    """오디오 데이터의 RMS(Root Mean Square) 값 계산"""
    count = len(block) / 2
    format = "%dh" % (count)
    try:
        shorts = struct.unpack(format, block)
        # 배열을 float32로 변환하여 오버플로우 방지
        shorts_array = np.array(shorts).astype(np.float32)
        sum_squares = np.sum(shorts_array ** 2)
        # 음수값이 발생하지 않도록 최소값을 0으로 설정
        rms = np.sqrt(max(0, sum_squares / count))
        return rms
    except Exception as e:
        print(f"오류 발생: {e}")
        return 0

def draw_volume_bar(screen, volume, max_volume):
    """볼륨에 따른 막대 게이지 그리기"""
    screen.fill(BLACK)
    
    # 볼륨 막대 배경
    pygame.draw.rect(screen, WHITE, (100, HEIGHT//2, BAR_WIDTH, BAR_HEIGHT), 2)
    
    # 볼륨 레벨에 비례하여 막대 길이 계산
    level = min(1.0, volume / max_volume)
    bar_length = int(BAR_WIDTH * level)
    
    # 강도에 따라 색상 변경 (낮을 때 녹색, 높을 때 빨간색)
    color = (int(255 * level), int(255 * (1 - level)), 0)
    
    # 볼륨 막대 그리기
    pygame.draw.rect(screen, color, (100, HEIGHT//2, bar_length, BAR_HEIGHT))
    
    # 텍스트 표시
    font = pygame.font.Font(None, 36)
    text = font.render(f"level: {int(level * 100)}%", True, WHITE)
    screen.blit(text, (100, HEIGHT//2 - 50))
    
    pygame.display.flip()

def main():
    # PyAudio 설정
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    # pygame 초기화
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("마이크 입력 레벨 모니터")
    clock = pygame.time.Clock()
    
    running = True
    
    # 볼륨 스무딩을 위한 변수들
    smoothed_volume = 0
    smoothing_factor = 0.3  # 낮을수록 부드러워짐
    
    # 초기 최대 볼륨
    max_volume = 3000  # 초기값
    
    try:
        while running:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # 오디오 데이터 읽기
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # 볼륨 레벨 계산
            rms = get_rms(data)
            
            # 볼륨 스무딩 (급격한 변화 완화)
            smoothed_volume = smoothing_factor * rms + (1 - smoothing_factor) * smoothed_volume
            
            # 최대 볼륨 자동 조정
            if smoothed_volume > max_volume * 0.8:
                max_volume = max(max_volume, smoothed_volume * 1.2)
            
            # 화면에 볼륨 막대 그리기
            draw_volume_bar(screen, smoothed_volume, max_volume)
            
            # 프레임 속도 제한
            clock.tick(30)
            
    finally:
        # 정리
        stream.stop_stream()
        stream.close()
        p.terminate()
        pygame.quit()

if __name__ == "__main__":
    main()