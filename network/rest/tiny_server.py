# %%
import socket
import json

from http_parser.http import HttpStream
from http_parser.reader import SocketReader

port = 8282
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", port))
server_socket.listen(5)  # 5 CONNECTION QUEUE

print(f'server bind {port}')

while True:
    print('wait connect')
    client_socket, addr = server_socket.accept()
    print(f'client connected {addr}')

    print('wait data')

    r = SocketReader(client_socket)
    p = HttpStream(r)
    
    print (p.url())
    print (p.method())
    print (p.headers()['Host'])

    # print (p.body_file().read())

    # data = client_socket.recv(1024)
    # print(f"recevied : \r\n {data.decode()}")

    _str = 'HTTP/1.1 200 OK\r\n'
    _str += 'Content-Type: Application/json\r\n\r\n'
    _str += json.dumps({"r": "ok", "code": 0,"msg" : "welcome"})

    client_socket.sendall(_str.encode())
    client_socket.close()

# %%
