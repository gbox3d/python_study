# %%
import socket
import json
import time
# from http_parser.http import HttpStream
# from http_parser.reader import SocketReader
from urllib.parse import urlparse, parse_qs
import yaml
# import argparse

#https://stackoverflow.com/questions/4685217/parse-raw-http-headers
from http.server import BaseHTTPRequestHandler
from io import BytesIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

#%%
with open( 'config.yaml' , 'r') as f:
    config_data = yaml.load(f,Loader=yaml.FullLoader)
    port = config_data['port']


# parser = argparse.ArgumentParser(description="argument parser sample")
# parser.add_argument('--port', type=int,
#                     default=100,
#                     help='help : it is test server')
# _args = parser.parse_args()

# #%%
# port = 8282
# if _args.port:
#     port = _args.port

#%%
print(f'server bind {port}')

try:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)  # 5 CONNECTION QUEUE

    _loop = True
    while _loop:
        print('wait connect')
        client_socket, addr = server_socket.accept()
        print(f'client connected {addr}')

        print('wait data')
        data = client_socket.recv(1024)

        print(data.decode())

        req = HTTPRequest(data)
        print(req.headers['Host'])
        print(req.headers.keys())

        print(f'method : {req.command}' )
        print(f'path : {req.path}')
        print(f'version : {req.request_version}')

        url = urlparse(req.path)
        print(url.path) # path

        query = parse_qs(url.query) # 인자값 분석 
        print(query)
        

        body_str = ""
        if url.path == '/exit' :
            _loop = False
            body_str = json.dumps({"r": "ok", "code": 0, "msg": "bye~"})
            _str = 'HTTP/1.1 200 OK\r\n'
            _str += 'Content-Type: Application/json\r\n'
            #cors 관련 처리 
            _str += 'Access-Control-Allow-Origin: *\r\n'
            _str += 'Access-Control-Allow-Methods: GET\r\n'
            _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
            _str += body_str
        elif url.path == '/hello':
            _name = query['name'][0]
            # print(f"name : {query['name'][0]}")
            body_str = json.dumps({"r": "ok", "code": 0, "msg": f"hello {_name}"})
            _str = 'HTTP/1.1 200 OK\r\n'
            _str += 'Content-Type: Application/json\r\n'
            #cors 관련 처리 
            _str += 'Access-Control-Allow-Origin: *\r\n'
            _str += 'Access-Control-Allow-Methods: GET\r\n'
            _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
            _str += body_str
        elif url.path == '/getimg':
            with open('hana1.jpg', 'rb') as f:
                _str = 'HTTP/1.1 200 OK\r\n'
                _str += 'Content-Type: image/jpg\r\n'
                #cors 관련 처리 
                _str += 'Access-Control-Allow-Origin: *\r\n'
                _str += 'Access-Control-Allow-Methods: GET\r\n'
                _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
                body_str = f.read()
                _str += body_str
                
        else :
            body_str = json.dumps({"r": "ok", "code": 0, "msg": "tiny http server"})
            _str = 'HTTP/1.1 200 OK\r\n'
            _str += 'Content-Type: Application/json\r\n'
            #cors 관련 처리 
            _str += 'Access-Control-Allow-Origin: *\r\n'
            _str += 'Access-Control-Allow-Methods: GET\r\n'
            _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
            _str += body_str

        client_socket.sendall(_str.encode())
        client_socket.close()

except KeyboardInterrupt as ki:
    # server_socket.close()
    print('exit by keybord')
except Exception as ex:
    print('Exception' , ex)

time.sleep(1)
server_socket.close()
time.sleep(1)
print('bye~')

# %%
