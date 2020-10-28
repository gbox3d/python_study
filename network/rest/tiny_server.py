# %%
import socket
import json

from http_parser.http import HttpStream
from http_parser.reader import SocketReader

from urllib.parse import urlparse, parse_qs

import argparse

parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument('--port', type=int,
                    default=100,
                    help='help : it is test server')
_args = parser.parse_args()

port = 8282
if _args.port:
    port = _args.port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", port))
server_socket.listen(5)  # 5 CONNECTION QUEUE

print(f'server bind {port}')

while True:
    print('wait connect')
    client_socket, addr = server_socket.accept()
    print(f'client connected {addr}')

    print('wait data')

    r = SocketReader(client_socket)
    p = HttpStream(r)

    url = urlparse(p.url())


    print(url.path) # path

    query = parse_qs(url.query) # 인자값 분석 
    print(query)
    print(f"name => {query['name'][0]}")

    print(p.method())
    print(p.headers())
    print("Host =>" + p.headers()['Host'])

    # print (p.body_file().read())

    # data = client_socket.recv(1024)
    # print(f"recevied : \r\n {data.decode()}")

    _str = 'HTTP/1.1 200 OK\r\n'
    _str += 'Content-Type: Application/json\r\n'
    #cors 관련 처리 
    _str += 'Access-Control-Allow-Origin: *\r\n'
    _str += 'Access-Control-Allow-Methods: GET\r\n'
    _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
    _str += json.dumps({"r": "ok", "code": 0, "msg": "welcome"})

    client_socket.sendall(_str.encode())
    client_socket.close()

# %%
