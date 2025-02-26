import time
import threading
from PIL import Image
import pystray

# 전역 플래그: 작업 실행 여부 제어용
is_running = False

def background_task():
    """백그라운드로 돌아가는 작업"""
    while True:
        if is_running:
            print("백그라운드 작업 실행 중...")
        time.sleep(2)  # 2초 간격으로 반복

def on_clicked_start(icon, item):
    """Start 메뉴 클릭 콜백"""
    global is_running
    is_running = True
    print("작업 시작!")

def on_clicked_stop(icon, item):
    """Stop 메뉴 클릭 콜백"""
    global is_running
    is_running = False
    print("작업 중지!")

def on_clicked_exit(icon, item):
    """Exit 메뉴 클릭 콜백"""
    icon.stop()  # 트레이 아이콘 정리 → 메인 스레드 종료
    print("프로그램 종료!")

def main():
    # 백그라운드 스레드 시작(daemon=True: 메인 스레드가 끝나면 함께 종료)
    t = threading.Thread(target=background_task, daemon=True)
    t.start()

    # 아이콘 이미지(예시로 간단히 빨간색으로 생성)
    image = Image.new('RGB', (32, 32), "red")

    # 트레이 메뉴 정의
    menu = pystray.Menu(
        pystray.MenuItem("Start", on_clicked_start),
        pystray.MenuItem("Stop", on_clicked_stop),
        pystray.MenuItem("Exit", on_clicked_exit)
    )

    # 트레이 아이콘 생성
    icon = pystray.Icon("TestTray", image, "트레이 예제", menu)

    # 트레이 아이콘 표시 및 이벤트 루프 진입 (블로킹 메서드)
    icon.run()

if __name__ == '__main__':
    main()
