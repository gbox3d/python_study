import asyncio
import struct
import json
from typing import Optional

# 기본 전역 락 (여러 연결이 동시에 쓰면 병목될 수 있으니, 가능하면 per-connection 락을 넘기세요)
write_lock = asyncio.Lock()

class ServerProtocol:
    # 보호 상수
    MAX_PAYLOAD_BYTES = 16 * 1024 * 1024   # 16MB
    MAX_HEADER_TIMEOUTS = 3                # 헤더 연속 타임아웃 상한

    # 상태코드
    SUCCESS = 0

    # ERR 코드 (치명적 문제)
    ERR_CHECKCODE_MISMATCH = 1
    ERR_INVALID_DATA = 2
    ERR_INVALID_REQUEST = 3
    ERR_INVALID_PARAMETER = 4
    ERR_INVALID_FORMAT = 5
    ERR_UNKNOWN_CODE = 8
    ERR_EXCEPTION = 9
    ERR_TIMEOUT = 10
    

    # WARN 코드 (비치명적 문제 경고)
    WARN_TIMEOUT = 100
    WARN_NO_DATA = 101
    WARN_NO_IMAGE = 102

    # 이미지 타입
    IMG_JPG = 0x00
    IMG_PNG = 0x01
    IMG_BMP = 0x02

    # REQ codes
    REQ_PING     = 99
    REQ_JSON     = 0x01           # c->s json (또는 범용 json 프레임)
    REQ_ACK      = 0x02           # c->s ack (header + req_code(4) + status(1))
    
    # PUSH codes (s->c json push 프레임)
    PUSH_JSON    = 0x03
    PUSH_STATUS  = 0x04
    PUSH_ALERT   = 0x05
    
    checkcode = 20251009  # 기본 체크코드 (변경 가능)

    # -------- 공통 쓰기 --------
    @staticmethod
    async def send_packet(writer: asyncio.StreamWriter, payload: bytes,
                          lock: Optional[asyncio.Lock] = None) -> None:
        lk = lock or write_lock
        async with lk:
            writer.write(payload)
            await writer.drain()

    # -------- ACK (header + req_code + status) --------
    @classmethod
    async def send_ack(cls, writer: asyncio.StreamWriter, req_code: int, status: int,
                       lock: Optional[asyncio.Lock] = None) -> None:
        # header: checkcode + REQ_ACK
        pkt_header = struct.pack("!II", cls.checkcode, cls.REQ_ACK)
        # body: req_code(4) + status(1)
        body = struct.pack("!IB", req_code, status)
        await cls.send_packet(writer, pkt_header + body, lock)

    @classmethod
    async def send_push_status(cls, writer: asyncio.StreamWriter, status: int,
                               lock: Optional[asyncio.Lock] = None) -> None:
        # header: checkcode + PUSH_STATUS
        pkt_header = struct.pack("!II", cls.checkcode, cls.PUSH_STATUS)
        # body: status(1) + reserved(15)
        body = struct.pack("!B15s", status, b'\x00' * 15)
        await cls.send_packet(writer, pkt_header + body, lock)

    @classmethod
    async def send_push_alert(cls, writer: asyncio.StreamWriter, alert_code: int,
                               lock: Optional[asyncio.Lock] = None) -> None:
        # header: checkcode + PUSH_ALERT
        pkt_header = struct.pack("!II", cls.checkcode, cls.PUSH_ALERT)
        # body: alert_code(1) + reserved(15)
        body = struct.pack("!B15s", alert_code, b'\x00' * 15)
        await cls.send_packet(writer, pkt_header + body, lock)

    # -------- JSON (header + size + body) --------
    @classmethod
    async def send_json(cls, writer: asyncio.StreamWriter, req_code: int, obj: dict,
                        lock: Optional[asyncio.Lock] = None) -> None:
        try:
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        except Exception as e:
            print(f"[WARN] JSON serialization error: {e}")
            return

        size = len(data)
        if size > cls.MAX_PAYLOAD_BYTES:
            print(f"[WARN] JSON payload too large to send: {size} > {cls.MAX_PAYLOAD_BYTES}")
            return

        # header: checkcode + req_code
        pkt_header = struct.pack("!II", cls.checkcode, req_code)
        size_bytes = struct.pack("!I", size)
        await cls.send_packet(writer, pkt_header + size_bytes + (data if size else b""), lock)


class ClientProtocol:
    
    # Request codes
    REQ_ACK      = 0x02           # c->s ack (header(8) + req_code(4) + status(1))

    @classmethod
    async def send_ack(cls, writer: asyncio.StreamWriter, checkcode: int,
                 req_code: int, status: int,
                 lock: Optional[asyncio.Lock] = None) -> None:

        pkt_header = struct.pack("!II", checkcode, cls.REQ_ACK)
        body = struct.pack("!IB", req_code, status)
        await ServerProtocol.send_packet(writer, pkt_header + body, lock)
