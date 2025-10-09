#############################
## filename : server.py
## 설명 : TCP Agent 중계 Server
## 작성자 : gbox3d
## 위 주석은 수정하지 마세요.
#############################

import asyncio
import struct
import json
import time
from typing import Optional

import itertools

from protocol import ServerProtocol,ClientProtocol

class Server:
    
    __VERSION__ = "0.0.1"

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 timeout: Optional[int] = None):
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else 8282
        self.timeout = timeout if timeout is not None else 10  # 초

        self.checkcode = ServerProtocol.checkcode

        print(f"Server version {self.__VERSION__}")
        print(f"Listening on {self.host}:{self.port}, timeout={self.timeout}s, checkcode={self.checkcode}")

        self._id_counter = itertools.count(1)  # 1,2,3,... 중복 없는 ID

    async def _read_exactly(self, reader: asyncio.StreamReader, n: int) -> bytes:
        return await asyncio.wait_for(reader.readexactly(n), timeout=self.timeout)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        header_timeouts = 0
        print(f"[INFO] 연결: {addr}")

        # ✅ 연결별 상태
        write_lock = asyncio.Lock()  # per-connection write lock

        try:

            await asyncio.sleep(0.5)  # 클라이언트가 준비할 시간

            conn_id = next(self._id_counter)
            # 최초 환영 메시지 전송
            _welcome_obj = {
                "cmd": "welcome",
                "version": self.__VERSION__,
                "server_time": int(time.time()),
                "id" : conn_id
            }
            await ServerProtocol.send_json(writer, ServerProtocol.PUSH_JSON, _welcome_obj, write_lock)  

            while True:
                # 8바이트: checkcode(uint32 BE) + request_code(uint32 BE)
                try:
                    header = await self._read_exactly(reader, 8)
                    checkcode, request_code = struct.unpack("!II", header)
                    header_timeouts = 0
                except asyncio.TimeoutError:
                    header_timeouts += 1
                    print(f"[WARN] TIMEOUT waiting header ({header_timeouts}/{ServerProtocol.MAX_HEADER_TIMEOUTS}) from {addr}")
                    
                    if header_timeouts >= ServerProtocol.MAX_HEADER_TIMEOUTS:
                        break

                    await ServerProtocol.send_push_alert(writer, ServerProtocol.WARN_TIMEOUT, write_lock)
                    continue

                if checkcode != self.checkcode:
                    print(f"[WARN] CHECKCODE mismatch: recv={checkcode}, expected={self.checkcode}")
                    await ServerProtocol.send_ack(writer, request_code, ServerProtocol.ERR_CHECKCODE_MISMATCH, write_lock)
                    break

                # --------------------
                # 99: ping
                # --------------------
                if request_code == ServerProtocol.REQ_PING:
                    print(f"[INFO] PING from {addr}")
                    # 단순 ACK 응답
                    await ServerProtocol.send_ack(writer, request_code, ServerProtocol.SUCCESS, write_lock)
                    continue

                # --------------------
                # 0x01: 제어 JSON 
                # --------------------
                elif request_code == ServerProtocol.REQ_JSON:
                    try:
                        size_bytes = await self._read_exactly(reader, 4)
                        (size,) = struct.unpack("!I", size_bytes)
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading size from {addr}")
                        await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_TIMEOUT, write_lock)
                        break

                    if size > ServerProtocol.MAX_PAYLOAD_BYTES:
                        print(f"[WARN] payload too large: {size} > {ServerProtocol.MAX_PAYLOAD_BYTES}")
                        await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_INVALID_DATA, write_lock)
                        break

                    try:
                        data = await self._read_exactly(reader, size) if size > 0 else b""
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading body({size}B) from {addr}")
                        await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_TIMEOUT, write_lock)
                        break

                    try:
                        print(f"[DEBUG] JSON data from {addr}: {data[:128].decode('utf-8', errors='ignore')}...")
                        obj = json.loads(data.decode('utf-8'))
                        if not isinstance(obj, dict):
                            raise ValueError("JSON root must be object")

                        msg = str(obj.get("msg", "")).lower()
                        
                        if msg == "push":
                            # 필요 시 확장 포인트
                            pass
                        elif msg == "pull":
                            # 필요 시 확장 포인트
                            pass
                        else:
                            await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_UNKNOWN_CODE, write_lock)
                            print(f"[WARN] unknown msg: {msg} from {addr}")
                            continue

                    except Exception:
                        await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_INVALID_FORMAT, write_lock)
                        continue

                    await ServerProtocol.send_ack(writer, request_code, ServerProtocol.SUCCESS, write_lock)

                # --------------------
                # 0x02: ACK (클라이언트->서버)
                # --------------------
                elif request_code == ClientProtocol.REQ_ACK:
                    try:
                        status_bytes = await self._read_exactly(reader, 5)
                        req_code, ack_status = struct.unpack("!IB", status_bytes)
                        print(f"[INFO] push ACK from {addr}: status={ack_status} for req_code={req_code}")
                    except asyncio.TimeoutError:
                        print(f"[WARN] TIMEOUT while reading push ACK from {addr}")
                        continue
                    except Exception as e:
                        print(f"[WARN] push ACK read error: {e}")
                        continue
                    continue

                # --------------------
                # 알 수 없는 요청
                # --------------------
                else:
                    print(f"[WARN] unknown request: {request_code} from {addr}")
                    await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_UNKNOWN_CODE, write_lock)

        except asyncio.IncompleteReadError:
            print(f"[INFO] EOF: {addr}")
        except asyncio.TimeoutError:
            print(f"[WARN] TIMEOUT: {addr}")
            try:
                await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_TIMEOUT, write_lock)
            except Exception:
                print(f"[WARN] Failed to send TIMEOUT status to {addr}")
        except Exception as e:
            print(f"[ERROR] 예외: {e}")
            try:
                await ServerProtocol.send_push_status(writer, ServerProtocol.ERR_EXCEPTION, write_lock)
            except Exception:
                print(f"[WARN] Failed to send EXCEPTION status to {addr}")
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            print(f"[INFO] 종료: {addr}")

    

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
