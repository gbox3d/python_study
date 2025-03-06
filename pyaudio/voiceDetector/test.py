from VoiceDetector import VoiceDetector
import time

def main():
    # VoiceDetector 초기화 (디버그 모드 활성화)
    detector = VoiceDetector(debug_mode=True)
    
    # 스트림 초기화 (기본 마이크 사용)
    detector.initialize_stream()
    
    print("VAD 테스트 시작... Ctrl+C로 종료")
    
    try:
        while True:
            # 오디오 데이터 읽기
            audio_data = detector.stream.read(detector.CHUNK, exception_on_overflow=False)
            
            # 음성 감지 (디버그 출력 자동으로 표시됨)
            detector.detect_speech(audio_data)
            
            # CPU 사용량 줄이기
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n테스트 종료")
    finally:
        # 리소스 정리
        detector.close_stream()

if __name__ == "__main__":
    main()