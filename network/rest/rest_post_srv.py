# %%
import socket
import json
import time
import base64

from urllib.parse import urlparse, parse_qs

from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

# import argparse

#나중에 참고하여 만들어보기 
#https://gist.github.com/yogendra/7585031

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

port = 8080
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
        data = client_socket.recv(10240)

        print(data.decode())

        req = HTTPRequest(data)
        print(req.headers['Host'])
        print(req.headers.keys())

        # print(f'method : {req.command}' )
        print(f'path : {req.path}')
        print(f'version : {req.request_version}')

        _method = req.command
        if _method == 'OPTIONS' :
            _method = req.headers['access-control-request-method']
        
        print(f'methos is {_method}')

        url = urlparse(req.path)
        print(url.path) # path

        if _method == 'GET':
            query = parse_qs(url.query) # 인자값 분석 
            print(query)
            

            # if url.path == '/exit' :
            #     _loop = False
            
            # elif url.path == '/hello':
            #     print(f"name : {query['name'][0]}")
            # else :
            #     pass
            
            if url.path == '/img' :
                _str = 'HTTP/1.1 200 OK\r\n'
                _str += 'Content-Type: image/jpeg\r\n'
                #cors 관련 처리 
                _str += 'Access-Control-Allow-Origin: *\r\n'
                _str += 'Access-Control-Allow-Methods: GET\r\n'
                _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
                
                
                with open('hana1.jpg', 'rb') as f:
                    # conver to base64
                    _str += base64.b64encode(f.read()).decode()
                
                
                
            else :
                _str = 'HTTP/1.1 200 OK\r\n'
                _str += 'Content-Type: Application/json\r\n'
                #cors 관련 처리 
                _str += 'Access-Control-Allow-Origin: *\r\n'
                _str += 'Access-Control-Allow-Methods: GET\r\n'
                _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
                _str += json.dumps({"r": "ok", "code": 0, "msg": "welcome"})

        elif _method == 'POST' :
            if url.path == '/upload':
                # _img = Image.open('../../res/bird1.jpg')
                # display(_img)
                print(req.headers['upload-name'])


            _str = 'HTTP/1.1 200 OK\r\n'
            _str += 'Content-Type: Application/json\r\n'
            #cors 관련 처리 
            _str += 'Access-Control-Allow-Origin: *\r\n'
            _str += 'Access-Control-Allow-Methods: POST\r\n'
            _str += 'Access-Control-Allow-Headers: upload-name ,content-type ,file-size\r\n'
            _str += 'Access-Control-Max-Age: 1000\r\n\r\n'
            _str += json.dumps({"r": "ok"})
        


        client_socket.sendall(_str.encode())
        client_socket.close()

except KeyboardInterrupt as ki:
    # server_socket.close()
    print('exit by keybord')
except Exception as ex:
    print(ex)

time.sleep(1)
server_socket.close()
time.sleep(1)
print('bye~')

# %%
