#############################
## filename : server.py
## 설명 : 간단한 TCP 서버 예제 (비동기, asyncio)
## 작성자 : gbox3d
## 위 주석은 수정하지 마세요.
#############################

import asyncio
import struct
import json
import time
from typing import Optional

class Server:
    # 상태코드
    SUCCESS = 0
    ERR_CHECKCODE_MISMATCH = 1
    ERR_INVALID_DATA = 2
    ERR_INVALID_REQUEST = 3
    ERR_INVALID_PARAMETER = 4
    ERR_INVALID_FORMAT = 5
    ERR_UNKNOWN_CODE = 8
    ERR_EXCEPTION = 9
    ERR_TIMEOUT = 10

    __VERSION__ = "1.0.2"

    # 보호 상수
    MAX_PAYLOAD_BYTES = 16 * 1024 * 1024   # 16MB
    MAX_HEADER_TIMEOUTS = 3                # 헤더 연속 타임아웃 상한

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 timeout: Optional[int] = None,
                 checkcode: Optional[int] = None):
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else 8282
        self.timeout = timeout if timeout is not None else 10  # 초
        self.checkcode = checkcode if checkcode is not None else 20251004

        print(f"Server version {self.__VERSION__}")
        print(f"Listening on {self.host}:{self.port}, timeout={self.timeout}s, checkcode={self.checkcode}")

    async def _read_exactly(self, reader: asyncio.StreamReader, n: int) -> bytes:
        return await asyncio.wait_for(reader.readexactly(n), timeout=self.timeout)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        header_timeouts = 0
        print(f"[INFO] 연결: {addr}")

        # ✅ 연결별 상태
        write_lock = asyncio.Lock()
        push_task: Optional[asyncio.Task] = None

        async def send_packet(payload: bytes):
            # 동시 write 경합을 방지
            async with write_lock:
                writer.write(payload)
                await writer.drain()

        async def send_status(req: int, status: int):
            await send_packet(struct.pack("!IIB", self.checkcode, req, status))

        try:
            while True:
                # 8바이트: checkcode(uint32 BE) + request_code(uint32 BE)
                try:
                    header = await self._read_exactly(reader, 8)
                    checkcode, request_code = struct.unpack("!II", header)
                    header_timeouts = 0
                except asyncio.TimeoutError:
                    header_timeouts += 1
                    print(f"[WARN] TIMEOUT waiting header ({header_timeouts}/{self.MAX_HEADER_TIMEOUTS}) from {addr}")
                    if header_timeouts >= self.MAX_HEADER_TIMEOUTS:
                        await send_status(0, self.ERR_TIMEOUT)
                        break
                    continue

                if checkcode != self.checkcode:
                    print(f"[WARN] CHECKCODE mismatch: recv={checkcode}, expected={self.checkcode}")
                    await send_status(request_code, self.ERR_CHECKCODE_MISMATCH)
                    break

                if request_code == 99:  # ping
                    await send_status(request_code, self.SUCCESS)
                    continue

                if request_code == 0x01:  # json string data (size(uint32) + data)
                    try:
                        size_bytes = await self._read_exactly(reader, 4)
                        (size,) = struct.unpack("!I", size_bytes)
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading size from {addr}")
                        await send_status(request_code, self.ERR_TIMEOUT)
                        break

                    if size > self.MAX_PAYLOAD_BYTES:
                        print(f"[WARN] payload too large: {size} > {self.MAX_PAYLOAD_BYTES}")
                        await send_status(request_code, self.ERR_INVALID_DATA)
                        break

                    try:
                        data = await self._read_exactly(reader, size) if size > 0 else b""
                        
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading body({size}B) from {addr}")
                        await send_status(request_code, self.ERR_TIMEOUT)
                        break

                    # JSON 파싱 및 명령 처리
                    try:
                        print(f"[DEBUG] JSON data from {addr}: {data[:128].decode('utf-8', errors='ignore')}...")
                        obj = json.loads(data.decode('utf-8'))
                        if not isinstance(obj, dict):
                            raise ValueError("JSON root must be object")

                        msg = str(obj.get("msg", "")).lower()
                        if msg == "start":
                            # 이미 돌고 있으면 재시작(취소 후 새로 시작)
                            if push_task and not push_task.done():
                                push_task.cancel()
                                try:
                                    await push_task
                                except asyncio.CancelledError:
                                    pass
                            push_task = asyncio.create_task(self.send_timepush(writer, write_lock))
                        elif msg == "stop":
                            if push_task and not push_task.done():
                                push_task.cancel()
                                try:
                                    await push_task
                                except asyncio.CancelledError:
                                    pass
                                push_task = None
                        else:
                            # 알 수 없는 msg 키
                            await send_status(request_code, self.ERR_INVALID_PARAMETER)
                            continue

                    except Exception:
                        await send_status(request_code, self.ERR_INVALID_FORMAT)
                        continue

                    await send_status(request_code, self.SUCCESS)
                    continue

                if request_code == 0x02:
                    # 👇 클라이언트 ACK 수신 (status 1B)
                    try:
                        status_bytes = await self._read_exactly(reader, 1)
                        (ack_status,) = struct.unpack("!B", status_bytes)
                        # 필요하면 통계/모니터링: ack_status 수집
                        print(f"[INFO] push ACK from {addr}: status={ack_status}")
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading push ACK from {addr}")
                        # ACK 실패는 치명적이지 않으므로 계속 루프
                        continue
                    except Exception as e:
                        print(f"[WARN] push ACK read error: {e}")
                        continue
                    # ACK에 대한 서버의 재응답은 없음(루프 방지)
                    continue

                # 알 수 없는 요청
                print(f"[WARN] unknown request: {request_code} from {addr}")
                await send_status(request_code, self.ERR_UNKNOWN_CODE)

        except asyncio.IncompleteReadError:
            print(f"[INFO] EOF: {addr}")
        except asyncio.TimeoutError:
            print(f"[WARN] TIMEOUT: {addr}")
        except Exception as e:
            print(f"[ERROR] 예외: {e}")
            try:
                await send_status(0, self.ERR_EXCEPTION)
            except Exception:
                pass
        finally:
            # ✅ 연결 종료 시 푸시 태스크 정리
            if push_task and not push_task.done():
                push_task.cancel()
                try:
                    await push_task
                except asyncio.CancelledError:
                    pass

            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            print(f"[INFO] 종료: {addr}")

    async def send_timepush(self, writer: asyncio.StreamWriter, write_lock: asyncio.Lock):
        """5초마다 epoch time을 JSON으로 s->c 푸시 (req_code = 0x02)"""
        try:
            while True:
                now = int(time.time())  # ✅ wall-clock epoch(sec)
                obj = {"time": now}
                body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
                header = struct.pack("!II", self.checkcode, 0x02)  # s->c push
                size   = struct.pack("!I", len(body))
                payload = header + size + body

                async with write_lock:
                    writer.write(payload)
                    await writer.drain()

                await asyncio.sleep(5)
        except asyncio.CancelledError:
            # 정상 취소 경로: 조용히 종료
            raise
        except Exception as e:
            print(f"[ERROR] Time push error: {e}")

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"[INFO] 서버 시작: {self.host}:{self.port}")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(Server().run())
    except KeyboardInterrupt:
        print("\n[INFO] 서버 종료")
