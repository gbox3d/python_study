import socket
import time

try:    
    # 1) 소켓 먼저 생성해 상태를 받을 준비
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 8890))

    # 2) Tello에 command 모드 보내기
    tello_addr = ('192.168.10.1', 8889)
    sock.sendto(b'command', tello_addr)

    # 3) Tello 응답 확인(= 'ok' 수신)
    sock.settimeout(3)
    data, addr = sock.recvfrom(1024)
    print("Command response:", data)
    
    
    # 4) 이후부터 상태 패킷을 기다림
    sock.settimeout(None)
    while True:
        data, addr = sock.recvfrom(1024)
        print("Received:", data, "from", addr)
    
    
except socket.timeout:
    print("No response for 'command'")

