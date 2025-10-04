#%%
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1",8282))
server_socket.listen(5) # 5 CONNECTION QUEUE

while True:
    print('wait connect')
    client_socket ,addr = server_socket.accept()
    print(f'client connected {addr}')

    print('wait data')

    while True:
        data = client_socket.recv(1024)
        if data == b'': break #fin

        print(f"recevied : {data}")
        print(f"recevied : {data.decode()}")

    #send 와 sendall의 차이는 모든 바이트가 전송되는 체크하느냐의 여부이다. send의 경우는 일부바이트가 빠져도 전송했다고 친다.
    client_socket.sendall('ok'.encode())
    client_socket.close()

# %%
