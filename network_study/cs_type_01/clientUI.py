import tkinter as tk
from tkinter import filedialog, messagebox

# app.py 상단 import에 추가
from io import BytesIO


import asyncio
import threading
from pathlib import Path

from protocol import ServerProtocol

from client import Client
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title("Canvas Image (Pillow)")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()


        # --- 네트워크 상태 ---
        self._loop: asyncio.AbstractEventLoop | None = None
        self._loop_thread: threading.Thread | None = None
        self.client: Client | None = None
        self._connected = False

    def build_ui(self):
        # --- UI ---
        top = tk.Frame(self); top.pack(fill="x")
        self.connect_button = tk.Button(top, text="Connect", command=self.Connect_network)
        self.connect_button.pack(side="left", padx=6, pady=6)

        # __init__ -> UI 섹션에 Ping 버튼 추가
        self.ping_button = tk.Button(top, text="Ping", command=self.ping_server)
        self.ping_button.pack(side="left", padx=6, pady=6)
        self.ping_button.config(state="disabled")

        self.status_var = tk.StringVar(value="Disconnected")
        tk.Label(top, textvariable=self.status_var).pack(side="right", padx=6)

        _frame1 = tk.Frame(self); _frame1.pack(fill="x")
        self.msg_var = tk.StringVar(value="Hi....")
        tk.Label(_frame1, text="message:").pack(side="left", padx=6)
        tk.Entry(_frame1, textvariable=self.msg_var).pack(side="left", fill="x", expand=True, padx=6)

        self.load_button = tk.Button(_frame1, text="Load", command=self.load_msg)
        self.load_button.pack(side="right", padx=6)
        self.load_button.config(state="disabled")

        self.save_button = tk.Button(_frame1, text="Save", command=self.save_msg)
        self.save_button.pack(side="right", padx=6)
        self.save_button.config(state="disabled")

        self.clear_button = tk.Button(_frame1, text="Clear", command=self.clear_msg)
        self.clear_button.pack(side="right", padx=6)
        self.clear_button.config(state="disabled")

    # ========== Async loop helpers ==========
    def _ensure_loop(self):
        if self._loop is not None:
            return
        self._loop = asyncio.new_event_loop()
        def _runner():
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        self._loop_thread = threading.Thread(target=_runner, daemon=True)
        self._loop_thread.start()

    def _run_async(self, coro, on_done=None):
        """백그라운드 루프에서 코루틴 실행. on_done(future) 콜백은 메인스레드에서 self.after로 호출."""
        self._ensure_loop()
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        if on_done:
            def _cb(f):
                # Tk는 메인스레드만 접근 가능
                self.after(0, on_done, f)
            fut.add_done_callback(_cb)
        return fut
    # ========================================

    

    def _on_connection_start(self,json_info: dict):

        if json_info is None:
            self.after(0, self._handle_disconnect, "Invalid server response")
            return
        if json_info["cmd"] == "welcome":
            info = f"version : {json_info['version']} , id : {json_info['id']}, connection time : {json_info['server_time']}"
            self.after(0, lambda: self.status_var.set(info))

            self._connected = True
            self.connect_button.config(state="normal")
            self.connect_button.config(text="Disconnect")
            self.ping_button.config(state="normal")

            self.save_button.config(state="normal")
            self.load_button.config(state="normal")
            self.clear_button.config(state="normal")
            
    def _on_connection_lost(self, reason: str):
        self.after(0, self._handle_disconnect, reason)

    def _disconnect(self):
        self._connected = False
        self.status_var.set("Disconnected")
        # self.status_info_var.set("Ready....")
        self.connect_button.config(state="normal")
        self.connect_button.config(text="Connect")
        self.client = None
        self.ping_button.config(state="disabled")

        self.save_button.config(state="disabled")
        self.load_button.config(state="disabled")
        self.clear_button.config(state="disabled")
    
    # 서버측에서 연결이 끊어진 경우 처리
    def _handle_disconnect(self, reason: str):
        if not self._connected:
            # 이미 끊어진 상태면 중복 처리 방지
            self.status_var.set("Disconnected")
        else:
            self._disconnect()

        messagebox.showwarning("Disconnected", f"서버 연결이 끊어졌습니다.\n\n{reason}")
    
    # 클라이언트 측에서 능동적으로 연결 해제
    def Disconnect_network(self):
        if not self._connected:
            return
        self.connect_button.config(state="disabled")
        self.status_var.set("Disconnecting...")

        def done(fut):
            try:
                fut.result()
            except Exception as e:
                messagebox.showerror("Disconnect failed", str(e))
            finally:
                self._disconnect()

        self._run_async(self.client.stop(), on_done=done)

    # ========== UI actions ==========
    def Connect_network(self):

        if self._connected:
            # messagebox.showinfo("Info", "Already connected.")
            self.Disconnect_network()
            return
        
        self.connect_button.config(state="disabled")
        self.status_var.set("Connecting...")

        ip = '127.0.0.1'
        port_str = '8282'
        
        self.client = Client(host=ip, port=int(port_str))

        # 콜백 등록
        self.client.on_connection_lost = self._on_connection_lost   # ← 등록
        self.client.on_connection_start = self._on_connection_start   # ← 등록

        def done(fut):
            try:
                if fut.result():  # bool
                    print(f"Connected to {ip}:{port_str}")
                    self.status_var.set("Waiting for server response...")
                else:
                    self.status_var.set("Disconnected")
                    messagebox.showwarning("Connect", "Server returned non-success status.")
                    self._connected = False

            except Exception as e:
                messagebox.showerror("Connect failed", str(e))
                self._connected = False
                self.status_var.set("Disconnected")
                self.connect_button.config(state="normal")
                self.connect_button.config(text="Connect")
        
        self._run_async(self.client.start(), on_done=done)

    # 메서드 추가
    def ping_server(self):
        
        self.ping_button.config(state="disabled")
        self.status_var.set("Pinging...")

        def done(fut):
            try:
                ok = fut.result()  # bool
                if ok:
                    self.status_var.set("Ping OK")
                else:
                    self.status_var.set("Ping FAIL")
                    messagebox.showwarning("Ping", "Server returned non-success status.")
            except Exception as e:
                self.status_var.set("Disconnected")
                messagebox.showerror("Ping failed", str(e))
            finally:
                # 연결 상태 유지 중이면 다시 활성화
                if self._connected:
                    self.ping_button.config(state="normal")

        self._run_async(self.client.send_ping(), on_done=done)

    def save_msg(self):
        self.save_button.config(state="disabled")
        msg = self.msg_var.get().strip()
        if not msg:
            messagebox.showwarning("Warning", "메시지를 입력하세요.")
            self.save_button.config(state="normal")
            return
        def done(fut):
            try:
                ok = fut.result()  # bool
                if ok:
                    self.status_var.set("Message saved.")
                    self.msg_var.set("")
                else:
                    self.status_var.set("Save FAIL")
                    messagebox.showwarning("Save", "Server returned non-success status.")
            except Exception as e:
                self.status_var.set("Disconnected")
                messagebox.showerror("Save failed", str(e))
            finally:
                # 연결 상태 유지 중이면 다시 활성화
                if self._connected:
                    print(f"[INFO] save_msg: ok")
                    self.save_button.config(state="normal")
        self._run_async(self.client.send_save_msg(msg), on_done=done)

    def load_msg(self):
        self.load_button.config(state="disabled")
        def done(fut):
            try:
                msg = fut.result()  # str
                if msg is not None:
                    self.msg_var.set(msg)
                    self.status_var.set("Message loaded.")
                else:
                    self.status_var.set("Load FAIL")
                    messagebox.showwarning("Load", "Server returned no message.")
            except Exception as e:
                self.status_var.set("Disconnected")
                messagebox.showerror("Load failed", str(e))
            finally:
                # 연결 상태 유지 중이면 다시 활성화
                if self._connected:
                    print(f"[INFO] load_msg: ok")
                    self.load_button.config(state="normal")
        self._run_async(self.client.send_load_msg(), on_done=done)

    def clear_msg(self):
        self.clear_button.config(state="disabled")
        def done(fut):
            try:
                ok = fut.result()  # bool
                if ok:
                    self.status_var.set("Message cleared.")
                    self.msg_var.set("")
                else:
                    self.status_var.set("Clear FAIL")
                    messagebox.showwarning("Clear", "Server returned non-success status.")
            except Exception as e:
                self.status_var.set("Disconnected")
                messagebox.showerror("Clear failed", str(e))
            finally:
                # 연결 상태 유지 중이면 다시 활성화
                if self._connected:
                    print(f"[INFO] clear_msg: ok")
                    self.clear_button.config(state="normal")

        self._run_async(self.client.send_clear_msg(), on_done=done)

    # ========== Shutdown ==========
    def on_close(self):
        async def _shutdown():
            if self.client:
                await self.client.stop()
        # 비동기 종료 스케줄
        if self._loop:
            asyncio.run_coroutine_threadsafe(_shutdown(), self._loop).result(timeout=3)
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._loop_thread:
                self._loop_thread.join(timeout=3)
        self.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()
