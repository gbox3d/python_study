"""
Voice Detector 모니터링 애플리케이션 실행 모듈
"""

from ui.AppUI import VoiceDetectorApp

def main():
    """메인 애플리케이션 실행"""
    app = VoiceDetectorApp()
    app.run()

if __name__ == "__main__":
    main()