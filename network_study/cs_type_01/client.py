#%% asyncio TCP client test app (ACK for REQ_PUSH)
import asyncio
import json
import struct
from typing import Dict, Optional

CHECKCODE = 20251004
REQ_PING  = 99
REQ_JSON  = 0x01
REQ_PUSH  = 0x02  # s->c push , c->s ACK

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8282

class TestClientApp:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, checkcode: int = CHECKCODE, timeout: float = 15.0):
        self.host = host
        self.port = port
        self.checkcode = checkcode
        self.timeout = timeout

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

        self.waiters: Dict[int, asyncio.Queue] = {
            REQ_PING: asyncio.Queue(),
            REQ_JSON: asyncio.Queue(),
        }

        self._recv_task: Optional[asyncio.Task] = None
        self._write_lock = asyncio.Lock()  # 👈 동시 write 보호
        self._closed = False

    async def start(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print(f"[CLIENT] connected -> {self.host}:{self.port}")
        self._recv_task = asyncio.create_task(self._recv_loop())

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

    async def _sendall(self, data: bytes):
        assert self.writer is not None
        async with self._write_lock:
            self.writer.write(data)
            await self.writer.drain()

    async def send_ping(self) -> int:
        header = struct.pack("!II", self.checkcode, REQ_PING)
        await self._sendall(header)
        status = await asyncio.wait_for(self.waiters[REQ_PING].get(), timeout=self.timeout)
        return status

    async def send_json(self, obj: dict) -> int:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        header = struct.pack("!II", self.checkcode, REQ_JSON)
        size   = struct.pack("!I", len(body))
        await self._sendall(header + size + body)
        status = await asyncio.wait_for(self.waiters[REQ_JSON].get(), timeout=self.timeout)
        return status

    async def send_push_ack(self, status: int = 0):
        """REQ_PUSH(0x02)에 대한 ACK 전송: header + status(1B)"""
        pkt = struct.pack("!IIB", self.checkcode, REQ_PUSH, status)
        await self._sendall(pkt)

    async def _recv_loop(self):
        try:
            while True:
                header = await self._read_exactly(8)
                r_check, r_req = struct.unpack("!II", header)

                if r_check != self.checkcode:
                    print(f"[CLIENT][WARN] checkcode mismatch: got={r_check}, expected={self.checkcode}")
                    return

                if r_req == REQ_PUSH:
                    # s->c push: size + body(JSON)
                    size_bytes = await self._read_exactly(4)
                    (size,) = struct.unpack("!I", size_bytes)
                    body = await self._read_exactly(size) if size > 0 else b""
                    try:
                        msg = json.loads(body.decode("utf-8"))
                    except Exception:
                        msg = {"raw": body[:128].hex()}
                    print(f"[PUSH] {msg}")

                    # 👇 즉시 ACK 전송 (status=0: SUCCESS)
                    try:
                        await self.send_push_ack(status=0)
                    except Exception as e:
                        print(f"[CLIENT][ERROR] push-ack send failed: {e}")
                    continue

                else:
                    # status only (1바이트)
                    status_bytes = await self._read_exactly(1)
                    (status,) = struct.unpack("!B", status_bytes)
                    q = self.waiters.get(r_req)
                    if q is not None:
                        q.put_nowait(status)
                    else:
                        print(f"[CLIENT][INFO] resp for req={r_req}, status={status}")
                    continue

        except asyncio.IncompleteReadError:
            print("[CLIENT][INFO] server closed connection")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[CLIENT][ERROR] recv_loop: {e}")

# 이하 REPL/메인 루프는 동일 (생략 가능)
async def ainput(prompt: str = "") -> str:
    return await asyncio.to_thread(input, prompt)

async def repl(app: TestClientApp):
    print("Commands: ping | start | stop | json {..} | help | quit")
    while True:
        cmdline = (await ainput("> ")).strip()
        if not cmdline: 
            continue
        if cmdline.lower() in ("quit","q","exit"): break
        if cmdline.lower() == "help":
            print("ping | start | stop | json {..} | quit"); continue
        if cmdline.lower() == "ping":
            print("[CMD][ping] status=", await app.send_ping()); continue
        if cmdline.lower() == "start":
            print("[CMD][start] status=", await app.send_json({"msg":"start"})); continue
        if cmdline.lower() == "stop":
            print("[CMD][stop] status=", await app.send_json({"msg":"stop"})); continue
        if cmdline.lower().startswith("json"):
            _, *rest = cmdline.split(" ", 1)
            raw = rest[0] if rest else "{}"
            try: obj = json.loads(raw)
            except Exception as e: print("[CMD][json] invalid:", e); continue
            print("[CMD][json] status=", await app.send_json(obj)); continue
        print(f"[REPL] unknown command: {cmdline}")

async def main():
    app = TestClientApp(DEFAULT_HOST, DEFAULT_PORT, CHECKCODE)
    try:
        await app.start()
        await repl(app)
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[CLIENT] KeyboardInterrupt")
