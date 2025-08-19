# tk_async_counters.py
import tkinter as tk
from tkinter import ttk
import threading
import asyncio
import queue

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tk + asyncio worker demo")
        self.geometry("360x220")
        self.resizable(False, False)

        # 상태값
        self.bg_count = 0         # 백그라운드(워커) 카운터
        self.btn_count = 0        # 버튼 클릭 카운터
        self._q = queue.Queue()   # 워커 -> Tk 데이터 전달
        self._running = False
        self._loop = None
        self._thread = None
        self._task = None

        self._build_ui()
        # Tk 스레드에서 주기적으로 큐 폴링 (스레드 세이프)
        self.after(50, self._poll_queue)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        r1 = ttk.Frame(root); r1.pack(fill="x", **pad)
        ttk.Label(r1, text="BG Count (async worker):").pack(side="left")
        self.lbl_bg = ttk.Label(r1, text="0"); self.lbl_bg.pack(side="left", padx=8)

        r2 = ttk.Frame(root); r2.pack(fill="x", **pad)
        ttk.Label(r2, text="Btn Count (UI thread):").pack(side="left")
        self.lbl_btn = ttk.Label(r2, text="0"); self.lbl_btn.pack(side="left", padx=8)
        ttk.Button(r2, text="Increment", command=self.inc_btn).pack(side="left")

        r3 = ttk.Frame(root); r3.pack(fill="x", **pad)
        self.btn_start = ttk.Button(r3, text="Start BG", command=self.start_worker)
        self.btn_stop  = ttk.Button(r3, text="Stop BG", command=self.stop_worker, state="disabled")
        self.btn_start.pack(side="left")
        self.btn_stop.pack(side="left", padx=8)

        self.lbl_status = ttk.Label(root, text="IDLE")
        self.lbl_status.pack(anchor="w", **pad)

    # --- UI 핸들러 ---
    def inc_btn(self):
        self.btn_count += 1
        self.lbl_btn.config(text=str(self.btn_count))

    def start_worker(self):
        if self._running:
            return
        self._running = True
        self.lbl_status.config(text="RUNNING")
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")

        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop_worker(self):
        if not self._running:
            return
        self.lbl_status.config(text="STOPPING...")

        # 워커 스레드의 asyncio 태스크를 안전하게 취소
        if self._loop and self._task:
            def _cancel():
                if not self._task.done():
                    self._task.cancel()
            self._loop.call_soon_threadsafe(_cancel)

        # 워커 스레드가 정리되도록 대기
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3.0)

        self._loop = None
        self._task = None
        self._thread = None
        self._running = False

        self.lbl_status.config(text="STOPPED")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

    def on_close(self):
        try:
            self.stop_worker()
        finally:
            self.destroy()

    # --- Tk 스레드에서 큐 폴링 (UI 갱신) ---
    def _poll_queue(self):
        try:
            while True:
                n = self._q.get_nowait()
                self.lbl_bg.config(text=str(n))
        except queue.Empty:
            pass
        finally:
            self.after(50, self._poll_queue)

    # --- 워커 스레드: asyncio 루프 + 코루틴 실행 ---
    def _worker(self):
        async def bg_counter():
            n = 0
            try:
                while True:
                    n += 1
                    self._q.put(n)        # Tk를 직접 건드리지 않고 큐로 전달
                    await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                # 필요 시 정리 로직
                raise

        async def runner():
            try:
                await bg_counter()       # 영구 루프
            except asyncio.CancelledError:
                pass
            finally:
                # run_forever를 탈출시키기 위해 stop
                if self._loop and self._loop.is_running():
                    self._loop.stop()

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._task = self._loop.create_task(runner())
        try:
            self._loop.run_forever()
        finally:
            if self._task and not self._task.done():
                self._task.cancel()
                try:
                    self._loop.run_until_complete(self._task)
                except Exception:
                    pass
            self._loop.close()

if __name__ == "__main__":
    App().mainloop()
