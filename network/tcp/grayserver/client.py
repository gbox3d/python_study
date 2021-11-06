
#%%
from io import BytesIO
from struct import *
import socket
import os
from time import sleep
import json


import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display

#%%
checkcode = 20211106
port = 20829
ip = 'localhost'
buff_size = 1024
img_file = ''

# %%
client_socket = socket.socket()
client_socket.connect((ip, port)) # 데이지서버의 끝자리 34 포트는 미러이미지 포트 

#웰컴 패킷 기다리기 
_r_data = client_socket.recv(4)
_p1,_,_,_ = unpack('<4B',_r_data)
# print(_p1)
if _p1 == 0x81 :
    print('welcome ok')

#%%

try :
    with open('./bus.jpg', 'rb') as fd:
        data = fd.read()
        print( f'file size {len(data)}')

        #요청 보내기 
        _header = pack('<L4BLB',checkcode,0x01,0,0,0,len(data),0)
        client_socket.sendall(_header + data)

        # 응답받기 
        _r_data = client_socket.recv(8)
        _checkcode,data_size = unpack('<LL',_r_data)
        print(f'{_checkcode},{data_size}')

        while _r_data.__sizeof__() < data_size + 8 :
            l = client_socket.recv(1024)
            if len(l) == 0: break;
            _r_data += l

        print(f'recv done {_r_data.__sizeof__() - data_size } ')
        _img = Image.open(BytesIO(_r_data[8:])) 
        
        display(_img)

# 소켓을 닫습니다.
    client_socket.close()

except Exception as ex :
    print('에러가 발생 했습니다', ex) 
    client_socket.close()
print('done')

# %%
