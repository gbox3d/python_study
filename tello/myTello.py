# file name : myTello.py
# date : 2025 2-21
# author : gbox3d
# description : tello 드론을 제어하는 모듈

import socket
import time
import threading

STATUS_PORT = 8890
CONTROL_PORT = 8889

class MyTello:
    def __init__(self, tello_ip="192.168.10.1", 
                 control_port=CONTROL_PORT, 
                 status_port=STATUS_PORT,
                 local_ip_cmd="",   # 명령 소켓 바인딩용, 기본 "" (모든 인터페이스)
                 local_ip_state=""):  # 상태 소켓 바인딩용, 기본 "" (모든 인터페이스)
        """
        MyTello 인스턴스를 초기화합니다.
        
        Parameters:
            tello_ip (str): Tello 드론의 IP 주소. 기본값 "192.168.10.1"
            control_port (int): 명령 전송 및 응답 수신에 사용할 포트. 기본값 8889.
            status_port (int): 상태 정보 수신에 사용할 포트. 기본값 8890.
            local_ip_cmd (str): 명령 소켓을 바인딩할 로컬 IP (기본: 모든 인터페이스).
            local_ip_state (str): 상태 소켓을 바인딩할 로컬 IP (기본: 모든 인터페이스).
        """
        self.tello_addr = (tello_ip, control_port)
        self.control_port = control_port
        self.status_port = status_port
        
        # 명령 전송 및 응답 수신용 소켓 생성
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((local_ip_cmd, control_port))
        
        # 상태 정보 수신용 소켓 생성
        self.state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.state_socket.bind((local_ip_state, status_port))
        
        # 스레드 종료를 위한 이벤트 객체
        self.stop_event = threading.Event()
        
        # 스레드 참조 변수
        self.response_thread = None
        self.state_thread = None

    def _udp_response_receiver(self):
        """Tello의 명령어 응답을 수신하는 내부 함수."""
        while not self.stop_event.is_set():
            try:
                data, address = self.client_socket.recvfrom(1024)
                print("Command response:", data.decode('utf-8', errors='ignore'), "from", address)
            except Exception as e:
                print("Response receiver error:", e)
                break

    def _udp_state_receiver(self):
        """Tello의 상태 정보를 수신하는 내부 함수."""
        self.state_socket.settimeout(1)
        while not self.stop_event.is_set():
            try:
                data, addr = self.state_socket.recvfrom(1024)
                #print("State received:", data.decode('utf-8', errors='ignore'), "from", addr)
            except socket.timeout:
                continue  # 타임아웃 발생 시 반복문의 처음으로 돌아감
            except Exception as e:
                print("State receiver error:", e)
                break
        self.state_socket.close()
        print("State receiver stopped.")

    def start(self):
        """명령 응답 및 상태 수신 스레드를 시작합니다."""
        self.response_thread = threading.Thread(target=self._udp_response_receiver)
        self.response_thread.daemon = True
        self.response_thread.start()

        self.state_thread = threading.Thread(target=self._udp_state_receiver)
        self.state_thread.daemon = True
        self.state_thread.start()
    
    def send_command(self, command):
        """
        Tello 드론에 명령어를 전송합니다.
        
        Parameters:
            command (str): Tello 드론에 보낼 명령어.
        """
        self.client_socket.sendto(command.encode('utf-8'), self.tello_addr)
    
    def send_status_start(self):
        """상태 정보 수신을 시작합니다."""
        self.state_socket.sendto(b'command', self.tello_addr)
        
    
    def close(self):
        """스레드를 종료하고 소켓을 닫습니다."""
        self.stop_event.set()
        if self.state_thread is not None:
            self.state_thread.join()
        self.client_socket.close()
        print("Exiting...")

if __name__ == "__main__":
    # 예제: Tello Wi-Fi 어댑터의 IP가 192.168.10.2인 경우
    # 필요한 경우 local_ip_cmd와 local_ip_state를 변경할 수 있습니다.
    tello = MyTello(local_ip_cmd="", local_ip_state="192.168.10.2")
    
    # 스레드 시작
    tello.start()
    
    print("Enter commands to send to Tello. Type 'quit' or 'exit' to stop.")
    
    try:
        while True:
            cmd = input("Command > ")
            if cmd.lower() in ("quit", "exit"):
                break
            tello.send_command(cmd)
    except KeyboardInterrupt:
        pass
    finally:
        tello.close()
