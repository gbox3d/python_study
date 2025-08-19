import asyncio
import threading
import queue
import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 상태 ---
        self._loop: asyncio.AbstractEventLoop | None = None
        self._task: asyncio.Task | None = None
        self._thread: threading.Thread | None = None
        self._ui_after_id = None
        self._q = queue.Queue()   # 워커→UI 이벤트 전달
        self._running = False

        # --- UI ---
        self.title("Asyncio x Tk (clean shutdown)")
        self.geometry("360x160")

        self.status_label = tk.Label(self, text="상태: 준비됨", font=("Arial", 14))
        self.status_label.pack(pady=16)

        btns = tk.Frame(self); btns.pack()
        tk.Button(btns, text="Start", command=self.start).pack(side="left", padx=6)
        tk.Button(btns, text="Stop",  command=self.stop).pack(side="left", padx=6)

        # 창 닫기 훅 (꼭 넣으세요)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # UI 폴링 루프 시작
        self._ui_tick()

    # --- 메인 스레드: 큐 폴링으로만 UI 갱신(스레드-세이프) ---
    def _ui_tick(self):
        try:
            while True:
                kind, value = self._q.get_nowait()
                if kind == "fg":
                    self.status_label.config(fg=value)
                elif kind == "text":
                    self.status_label.config(text=value)
        except queue.Empty:
            pass
        finally:
            # 50ms 주기 폴링
            self._ui_after_id = self.after(50, self._ui_tick)

    # --- 워커 스레드(이벤트 루프 보유) ---
    def _worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop

        async def runner():
            try:
                self._q.put(("text", "상태: 동작중"))
                while True:
                    # UI 호출은 금지! -> 큐에 넣고, Tk가 _ui_tick에서 처리
                    self._q.put(("fg", "red"))
                    await asyncio.sleep(0.3)
                    self._q.put(("fg", "black"))
                    await asyncio.sleep(0.3)
            except asyncio.CancelledError:
                # 필요한 정리 로직
                pass
            finally:
                # run_forever 종료 트리거
                if loop.is_running():
                    loop.stop()
                # UI에 마지막 상태 전달
                self._q.put(("text", "상태: 정지됨"))

        self._task = loop.create_task(runner())
        try:
            loop.run_forever()
        finally:
            # 남은 태스크 정리
            if self._task and not self._task.done():
                self._task.cancel()
                try:
                    loop.run_until_complete(self._task)
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
            loop.close()

    # --- 제어 ---
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        # 워커 루프에 취소 지시 (스레드-세이프)
        if self._loop and self._task:
            self._loop.call_soon_threadsafe(self._task.cancel)

        # 워커 스레드 종료 대기
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3.0)

        self._loop = None
        self._task = None
        self._thread = None

        # UI after 타이머도 정리(원하면 계속 유지해도 되지만 종료 시에는 취소가 깔끔)
        if self._ui_after_id is not None:
            try:
                self.after_cancel(self._ui_after_id)
            except Exception:
                pass
            self._ui_after_id = None

        print("Application stopped.")

    def on_close(self):
        # 창 닫기(X)에서도 반드시 정리
        try:
            self.stop()
        finally:
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
