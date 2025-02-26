import socket
import requests

# 1️⃣ Tello 상태 패킷 수신 테스트
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8890))

tello_addr = ('192.168.10.1', 8889)
sock.sendto(b'command', tello_addr)

print("Tello is in command mode!")

# 2️⃣ 인터넷 연결 테스트 (ChatGPT API 호출)
try:
    response = requests.get("https://api.openai.com/v1/models")
    print("✅ 인터넷 연결 정상!")
except requests.exceptions.RequestException as e:
    print("❌ 인터넷 연결 실패!", e)

# 3️⃣ 상태 패킷 출력
sock.settimeout(5)
try:
    while True:
        data, addr = sock.recvfrom(1024)
        #print("Tello Status:", data.decode())
        print("Tello Status:", data.decode(errors='ignore'))

except socket.timeout:
    print("No state packets received!")
