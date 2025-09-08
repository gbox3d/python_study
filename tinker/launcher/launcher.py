# improved_main.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import importlib
import traceback
import time
import queue

WINDOW_SIZE = (400, 280)

class ImprovedStartWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Miracle ASR Server ver. 1.0")
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.resizable(False, False)
        
        # 창을 화면 중앙에 배치
        self.center_window()
        
        try:
            self.iconbitmap('icon.ico')
        except:
            pass  # 아이콘 파일이 없어도 무시

        # UI 구성
        self.setup_ui()
        
        # 워커와 통신용 큐
        self.progress_queue = queue.Queue()
        self.error_queue = queue.Queue()
        
        # 창 닫기 이벤트
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # 워커 결과 저장
        self._app_class = None
        self._worker_thread = None
        self._cancelled = False

    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (WINDOW_SIZE[0] // 2)
        y = (self.winfo_screenheight() // 2) - (WINDOW_SIZE[1] // 2)
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{x}+{y}")

    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 로고/제목
        title_label = tk.Label(
            main_frame, 
            text="Miracle ASR MCP",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # 상태 메시지
        self.status_label = tk.Label(
            main_frame,
            text="초기화를 준비하고 있습니다...",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=(0, 15))
        
        # 프로그레스 바
        self.progress = ttk.Progressbar(
            main_frame,
            mode="determinate",  # determinate로 변경
            length=300
        )
        self.progress.pack(pady=(0, 10))
        
        # 백분율 표시
        self.percent_label = tk.Label(
            main_frame,
            text="0%",
            font=('Arial', 9),
            bg='white',
            fg='#95a5a6'
        )
        self.percent_label.pack()
        
        # 취소 버튼 (선택사항)
        self.cancel_btn = tk.Button(
            main_frame,
            text="취소",
            command=self._on_close,
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20
        )
        self.cancel_btn.pack(pady=(15, 0))

    def start(self):
        """로딩 시작"""
        # 워커 스레드 시작
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
        
        # 진행상황 모니터링 시작
        self.monitor_progress()
        
        # 스플래시 메인루프
        self.mainloop()

    def monitor_progress(self):
        """워커 스레드의 진행상황 모니터링"""
        try:
            # 진행상황 업데이트 확인
            while True:
                progress_data = self.progress_queue.get_nowait()
                self.update_progress(progress_data['percent'], progress_data['message'])
        except queue.Empty:
            pass
        
        try:
            # 에러 확인
            error_msg = self.error_queue.get_nowait()
            self._on_worker_error(error_msg)
            return
        except queue.Empty:
            pass
        
        # 워커가 완료되었는지 확인
        if self._worker_thread and not self._worker_thread.is_alive():
            if not self._cancelled and self._app_class:
                self._launch_main()
            return
        
        # 100ms 후 다시 확인
        if not self._cancelled:
            self.after(100, self.monitor_progress)

    def update_progress(self, percent, message):
        """진행상황 업데이트"""
        self.progress['value'] = percent
        self.percent_label.config(text=f"{percent}%")
        self.status_label.config(text=message)
        self.update_idletasks()

    def _worker(self):
        """백그라운드 작업 수행"""
        try:
            steps = [
                (10, "step 1: todo.."),
                (30, "step 2: checking torch..."),
                (50, "step 3: loading appUi..."),
                (70, "step 4: initializing..."),
                (90, "step 5: finalizing..."),
                (100, "완료!")
            ]

            for percent, message in steps:
                if self._cancelled:
                    return
                
                # 진행상황 업데이트
                self.progress_queue.put({
                    'percent': percent,
                    'message': message
                })

                if percent == 10:
                    # 예시: torch 관련 검사
                    time.sleep(0.5)  # 시뮬레이션
                elif percent == 30:
                    # 예시: 앱 UI 로딩
                    time.sleep(0.5)
                elif percent == 50:
                    # 예시: 앱 초기화
                    time.sleep(0.5)
                elif percent == 70:
                    # 예시: 추가적인 초기화 작업
                    self._app_class = importlib.import_module('app').App
                    time.sleep(0.5)
                    
                elif percent == 90:
                    # 예시: 최종화 작업
                    time.sleep(0.5)
                elif percent == 100:    
                    # 앱 클래스 로딩
                    try:
                        self._app_class = importlib.import_module('app').App
                    except ImportError as e:
                        self.error_queue.put(f"앱 모듈 로딩 실패: {e}")
                        return
                    
                time.sleep(0.2)  # 각 단계별 최소 시간
            
        except Exception as e:
            if not self._cancelled:
                self.error_queue.put(traceback.format_exc())

    def _launch_main(self):
        """메인 애플리케이션 실행"""
        try:
            self.destroy()  # 스플래시 닫기
            
            # 메인 앱 실행
            app = self._app_class()
            app.run()
            
        except Exception as e:
            messagebox.showerror("실행 오류", str(e))

    def _on_worker_error(self, error_text):
        """워커 에러 처리"""
        self.update_progress(0, "오류가 발생했습니다.")
        messagebox.showerror("초기화 오류", error_text)
        self.destroy()

    def _on_close(self):
        """창 닫기 처리"""
        self._cancelled = True
        self.destroy()


if __name__ == "__main__":
    # 개선된 스플래시 사용
    ImprovedStartWindow().start()