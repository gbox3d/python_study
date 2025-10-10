#######################################
# filename: client.py
# author: gbox3d
# 위 주석은 수정하지 마시오
#######################################

import asyncio
import json
import struct
from typing import Dict, Optional, Union
from pathlib import Path
import time
from typing import Dict, Optional, Union, Callable   # ← Callable 추가
from protocol import ServerProtocol,ClientProtocol

from collections import defaultdict

class Client:
    def __init__(self, host: str, port: int,
                 checkcode:int = ServerProtocol.checkcode, timeout: float = 15.0):
        self.host = host
        self.port = port
        self.checkcode = checkcode
        self.timeout = timeout

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

        self._recv_task: Optional[asyncio.Task] = None
        self._write_lock = asyncio.Lock()   # 동시 write 보호
        self._closed = False

        self.waiters: dict[int, asyncio.Queue] = defaultdict(asyncio.Queue)
        
        self.on_connection_start: Optional[Callable[[str], None]] = None  # ← 추가
        self.on_connection_lost: Optional[Callable[[str], None]] = None  # ← 추가

        

    def _notify_connect(self, json_info: dict):
        cb = self.on_connection_start
        if cb:
            try:
                cb(json_info)  # UI 쪽에서 after로 래핑하여 안전 처리
            except Exception as e:
                print(f"[CLIENT][WARN] on_connection_start callback error: {e}")    

    def _notify_disconnect(self, reason: str):
        cb = self.on_connection_lost
        if cb:
            try:
                cb(reason)  # UI 쪽에서 after로 래핑하여 안전 처리
            except Exception as e:
                print(f"[CLIENT][WARN] on_connection_lost callback error: {e}")

    async def start(self) -> bool:
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port) # 연결 시도
            print(f"[CLIENT] connected -> {self.host}:{self.port}")
            self._recv_task = asyncio.create_task(self._recv_loop()) # 수신 루프 시작

            return True

        except Exception as e:
            print(f"[CLIENT] failed to connect: {str(e)}")
            raise ConnectionError(f"failed to connect to {self.host}:{self.port}") from e

    async def stop(self):
        if self._closed:
            return
        self._closed = True
        if self._recv_task and not self._recv_task.done():
            self._recv_task.cancel()
            try:
                await self._recv_task
            except asyncio.CancelledError:
                pass
        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except Exception:
                pass
        print("[CLIENT] closed")

    async def _read_exactly(self, n: int) -> bytes:
        assert self.reader is not None
        return await asyncio.wait_for(self.reader.readexactly(n), timeout=self.timeout)
    
    # ---------- 기본 요청 ----------
    async def send_ping(self) -> bool:
        header = struct.pack("!II", self.checkcode, ServerProtocol.REQ_PING)
        await ServerProtocol.send_packet(self.writer, header, self._write_lock)
        
        # 응답은 _recv_loop가 받아서 큐에 넣어줌

        status = await asyncio.wait_for(
            self.waiters[ServerProtocol.REQ_PING].get(),
            timeout=self.timeout
        )
        return status == ServerProtocol.SUCCESS
  
    async def send_save_msg(self, msg: str) -> bool:

        req_obj = {
            "cmd": "save_msg",
            "msg": msg,
            "timestamp": int(time.time())
        }

        await ServerProtocol.send_json(self.writer, ServerProtocol.REQ_JSON, req_obj, self._write_lock)

        status = await asyncio.wait_for(
            self.waiters[ServerProtocol.REQ_JSON].get(),
            timeout=self.timeout
        )
        return status == ServerProtocol.SUCCESS
    
    async def send_load_msg(self) -> Optional[str]:

        req_obj = {
            "cmd": "load_msg",
            "timestamp": int(time.time())
        }

        await ServerProtocol.send_json(self.writer, ServerProtocol.REQ_JSON, req_obj, self._write_lock)

        strMsg = await asyncio.wait_for(
            self.waiters[ServerProtocol.PUSH_JSON].get(),
            timeout=self.timeout
        )

        return strMsg if strMsg else None
        
    async def send_clear_msg(self) -> bool:

        req_obj = {
            "cmd": "clear_msg",
            "timestamp": int(time.time())
        }

        await ServerProtocol.send_json(self.writer, ServerProtocol.REQ_JSON, req_obj, self._write_lock)

        status = await asyncio.wait_for(
            self.waiters[ServerProtocol.REQ_JSON].get(),
            timeout=self.timeout
        )
        return status == ServerProtocol.SUCCESS

    # ---------- 수신 루프 ----------
    async def _recv_loop(self):
        try:
            while True:
                try:
                    header = await self._read_exactly(8)
                except asyncio.TimeoutError:
                    print("[CLIENT][WARN] recv timeout"); continue

                r_check, r_req = struct.unpack("!II", header)
                if r_check != self.checkcode:
                    print(f"[CLIENT][WARN] checkcode mismatch: got={r_check}, expected={self.checkcode}")
                    return
                
                print(f"[CLIENT] recv: req={r_req}")

                if r_req == ServerProtocol.PUSH_JSON:
                    size = struct.unpack("!I", await self._read_exactly(4))[0]
                    body = await self._read_exactly(size) if size>0 else b""
                    try:
                        obj_data = json.loads(body.decode("utf-8"))
                    except Exception:
                        obj_data = {"raw": body[:128].hex()}

                    print(f"[PUSH JSON] {obj_data}")

                    if "cmd" in obj_data :
                        if obj_data["cmd"] == "welcome":
                            self._notify_connect(obj_data)
                        elif obj_data["cmd"] == "load_msg":
                            q = self.waiters.get(ServerProtocol.PUSH_JSON)
                            if q:

                                msg = obj_data.get("msg","")
                                self.waiters[ServerProtocol.PUSH_JSON].put_nowait(msg)
                                continue
                            else:
                                print(f"[CLIENT][INFO] PUSH_JSON for load_msg (no waiter)")

                    # 즉시 ACK
                    try:
                        await ClientProtocol.send_ack(
                            writer=self.writer,
                            checkcode=self.checkcode,
                            req_code=ServerProtocol.PUSH_JSON,
                            status=ServerProtocol.SUCCESS,
                            lock=self._write_lock
                        )
                    except Exception as e:
                        print(f"[CLIENT][ERROR] push-ack send failed: {e}")
                    continue

                elif r_req == ServerProtocol.REQ_ACK:

                    code_bytes = await self._read_exactly(16)  # req_code(4) + status(1) + reserved(11)
                    (_res_code,status) = struct.unpack("!IB", code_bytes[:5])
                    
                    q = self.waiters.get(_res_code)
                    if q:
                        q.put_nowait(status)
                    else:
                        print(f"[CLIENT][INFO] ACK for res_code={_res_code}, status={status} (no waiter)")
                        continue
                elif r_req == ServerProtocol.PUSH_ALERT:

                    body = await self._read_exactly(16)  # alert_code(1) + reserved(15)
                    (status,) = struct.unpack("!B", body[:1])

                    print(f"[CLIENT][ALERT] server alert: code={status}")
                    continue
                elif r_req == ServerProtocol.PUSH_STATUS:
                    body = await self._read_exactly(16)  # status_code(1) + reserved(15)
                    (status,) = struct.unpack("!B", body[:1])
                    print(f"[CLIENT][STATUS] server status update: code={status}")
                    continue
                else:
                    print(f"[CLIENT][WARN] unknown req code: {r_req}")

        except asyncio.IncompleteReadError:
            print("[CLIENT][INFO] server closed connection")
            self._notify_disconnect("서버와의 연결이 끊어졌습니다.")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[CLIENT][ERROR] recv_loop: {e}")
