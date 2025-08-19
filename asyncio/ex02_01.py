# tk_async_min.py
import tkinter as tk
import threading
import asyncio

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minimal Tk + asyncio")
        self.geometry("260x120")

        # 표시용 변수
        self.var = tk.StringVar(value="0")

        # UI 최소 구성
        tk.Label(self, text="Count:").pack(pady=(12, 0))
        tk.Label(self, textvariable=self.var, font=("Arial", 20)).pack()
        btns = tk.Frame(self); btns.pack(pady=8)
        tk.Button(btns, text="Start", command=self.start_worker).pack(side="left", padx=5)
        tk.Button(btns, text="Stop",  command=self.stop_worker).pack(side="left", padx=5)

        # 상태(워커/루프/태스크)
        self._running = False
        self._thread = None
        self._loop   = None
        self._task   = None

        # 창 닫기 시 정리
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_worker(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop_worker(self):
        if not self._running:
            return
        # 워커 스레드의 이벤트 루프에 "취소"를 스레드-세이프로 요청
        if self._loop and self._task:
            def _cancel():
                if not self._task.done():
                    self._task.cancel()
            self._loop.call_soon_threadsafe(_cancel)

        # 워커 정리 대기 (짧게)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        self._running = False
        self._thread = None
        self._loop   = None
        self._task   = None

    def on_close(self):
        try:
            self.stop_worker()
        finally:
            self.destroy()

    # ---------------- 워커 스레드 ----------------
    def _worker(self):
        async def counter():
            n = 0
            try:
                while True:
                    n += 1
                    # Tk UI 갱신은 메인 스레드에서만! -> after로 안전하게 위임
                    self.after(0, lambda v=n: self.var.set(str(v)))
                    await asyncio.sleep(0.3)
            except asyncio.CancelledError:
                # 필요 시 정리 작업 가능
                raise

        async def runner():
            try:
                await counter()   # 무한 루프
            except asyncio.CancelledError:
                pass
            finally:
                # run_forever 탈출
                if self._loop and self._loop.is_running():
                    self._loop.stop()

        # ★ 핵심: 이 스레드 전용 이벤트 루프 생성 & 등록 이밴트 루프 시작 ---->
        self._loop = asyncio.new_event_loop()   # 새 루프를 만들고
        asyncio.set_event_loop(self._loop)      # 이 스레드의 현재 루프로 등록

        # 카운터 코루틴을 태스크로 올린 뒤 루프 실행
        self._task = self._loop.create_task(runner())
        try:
            self._loop.run_forever()
        finally:
            # 정리: 태스크가 남아있으면 취소하고 종료까지 대기
            if self._task and not self._task.done():
                self._task.cancel()
                try:
                    self._loop.run_until_complete(self._task)
                except Exception:
                    pass
            self._loop.close() # 이벤트 루프 닫기 <-----

if __name__ == "__main__":
    App().mainloop()
