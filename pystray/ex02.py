import tkinter as tk
import time
import threading
import os
import yaml  # pip install pyyaml 필요
from PIL import Image
import pystray

class Application:
    def __init__(self):
        # 설정 파일 및 기본값 정의
        self.settings_file = "settings.yaml"
        self.default_settings = {"task_speed": 2.0}
        self.task_speed = self.default_settings["task_speed"]
        self.is_running = False

        # 설정 로드 (파일 없으면 기본값 사용)
        self.load_settings()

        # tkinter 루트 생성 (메인 창은 숨김)
        self.root = tk.Tk()
        self.root.withdraw()

        # pystray 아이콘 생성
        self.icon = self.create_tray_icon()

        # 백그라운드 작업 스레드 시작 (daemon)
        self.bg_thread = threading.Thread(target=self.background_task, daemon=True)
        self.bg_thread.start()

        # 트레이 아이콘 실행을 위한 스레드 시작 (블로킹이므로 별도 실행)
        self.tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
        self.tray_thread.start()

    def load_settings(self):
        """YAML 파일에서 설정값을 로드 (파일이 없으면 기본값 사용)"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = yaml.safe_load(f)
                if settings is None:
                    settings = {}
                self.task_speed = settings.get("task_speed", self.default_settings["task_speed"])
                print(f"설정 로드 완료: task_speed = {self.task_speed}초")
        else:
            self.task_speed = self.default_settings["task_speed"]
            print("설정 파일이 없어 기본값을 사용합니다.")

    def save_settings(self):
        """현재 설정값을 YAML 파일로 저장"""
        settings = {"task_speed": self.task_speed}
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            yaml.dump(settings, f, default_flow_style=False, allow_unicode=True)
        print(f"설정 저장 완료: task_speed = {self.task_speed}초")

    def background_task(self):
        """백그라운드로 실행되는 작업 (is_running True일 때만 동작)"""
        while True:
            if self.is_running:
                print(f"백그라운드 작업 실행 중... (속도: {self.task_speed}초)")
                time.sleep(self.task_speed)
            else:
                time.sleep(0.5)

    def on_start(self, icon, item):
        self.is_running = True
        print("작업 시작!")

    def on_stop(self, icon, item):
        self.is_running = False
        print("작업 중지!")

    def on_settings(self, icon, item):
        self.create_settings_window()

    def on_exit(self, icon, item):
        print("종료 처리 중...")
        self.icon.stop()    # pystray 아이콘 종료
        # 메인 스레드에서 tkinter 종료 처리 예약
        self.root.after(0, self.root.destroy)
        

    def create_settings_window(self):
        """설정 창을 생성하여 작업 속도를 변경 및 저장"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("설정 창")

        tk.Label(settings_window, text="작업 속도(초):").grid(row=0, column=0, padx=10, pady=10)
        speed_var = tk.DoubleVar(value=self.task_speed)
        speed_entry = tk.Entry(settings_window, textvariable=speed_var)
        speed_entry.grid(row=0, column=1, padx=10, pady=10)

        def on_save():
            self.task_speed = speed_var.get()
            print(f"설정 변경: task_speed = {self.task_speed}초")
            self.save_settings()
            settings_window.destroy()

        save_button = tk.Button(settings_window, text="저장", command=on_save)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_tray_icon(self):
        """pystray 아이콘 및 메뉴 생성"""
        # 예시로 파란색 32x32 아이콘 생성
        icon_image = Image.new('RGB', (32, 32), color="blue")
        menu = pystray.Menu(
            pystray.MenuItem("Start", self.on_start),
            pystray.MenuItem("Stop", self.on_stop),
            pystray.MenuItem("Settings", self.on_settings),
            pystray.MenuItem("Exit", self.on_exit)
        )
        icon = pystray.Icon("TrayApp", icon_image, "트레이 예제", menu)
        return icon

    def run_tray_icon(self):
        """트레이 아이콘 이벤트 루프 실행"""
        self.icon.run()

    def run(self):
        """tkinter 메인 루프 실행 (프로그램 진입점)"""
        self.root.mainloop()


if __name__ == '__main__':
    app = Application()
    app.run()
