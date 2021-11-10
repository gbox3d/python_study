#%%
#load b ase mosdule
import socket
import io
from struct import *
import argparse
import time
import json
import yaml
import numpy as np

import sys

from PIL import Image, ImageDraw, ImageFont
from IPython.display import display


import cv2 as cv

# from modules.etc import isnotebook,NumpyJsonEncoder

appVersion = [0,0,1]
print(f'start app version {appVersion}')

#%% load config
checkcode = 20211106
port = 20829
ip = 'localhost'
# model_type = 'yolov5'
# model_path = '../../yolov5/yolov5s.pt'
buff_size = 1024
#%%
parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument(
    '-p','--port', type=int, 
    default=port,
    help='help : port')
parser.add_argument('-i','--ip', type=str, 
    default=ip,
    help='help : ip address')

_args = parser.parse_args()

ip = _args.ip
port = _args.port


# %% init network
print(f'ip : {_args.ip} , port : {_args.port}')
try :
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)  # 5 CONNECTION QUEUE

    print(f'start object detecor version : {appVersion[0]} {appVersion[1]} {appVersion[2]} , port : {port}')
except Exception as ex:
    print(ex)
    time.sleep(5)
    exit()

#%%
while True:
    try:
        print('wait connect')
        
        client_socket, addr = server_socket.accept()
        
        # if debug_log == True:
        print(f'client connected {addr}')

        _welcome_pkt = pack('<4B',0x81,0,0,0)
        client_socket.sendall(_welcome_pkt)

        print('wait data')

        header = client_socket.recv(buff_size) # header size 16

        _checkcode,_cmd,_cmd_p1,_cmd_p2,_cmd_p3  = unpack('<LBBBB',header[:8])
        print(_checkcode,_cmd)

        if _checkcode == checkcode :

            if _cmd == 0x01 : #req detect
                _data_size,_ = unpack('<LB',header[8:13])
                _data = header[13:]
                
                print(f'target data size : {_data_size}')
                print(f'current data size : {_data.__sizeof__()}')

                #파이썬의 빈 바이트 버퍼 크기는 33이다.(실제 바이트 수에서 33을 더해준 값이다.)
                while len(_data) < _data_size :
                # while True :
                # while _data.__sizeof__() < _data_size + 33 :
                    l = client_socket.recv(buff_size)
                    # if len(l) == 0 : break;
                    print(l.__sizeof__() ,len(l) )
                    _data += l

                print(f'recv done : {len(_data)} , {_data_size} ')

                print('img cvt gray')
                img =  np.array(Image.open(io.BytesIO(_data)) )
                img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
                _img = cv.resize(img,dsize=(0,0),fx=0.25,fy=0.25,interpolation=cv.INTER_AREA)
                encode_param=[int(cv.IMWRITE_JPEG_QUALITY),90]
                _,_encodee_img = cv.imencode('.jpg',_img,encode_param)

                __encodee_img_byte = _encodee_img.tobytes() # np.array를 bytes로 변환 

                _res_packet_header = pack('<LL',checkcode,__encodee_img_byte.__sizeof__()) # 8 byte
                client_socket.sendall(_res_packet_header + __encodee_img_byte)
                # client_socket.sendall(_encodee_img)
                
            elif _cmd == 0x99 : # req close 
                _r_str = json.dumps({'r':'ok','msg':'close'})
                print(_r_str)
                client_socket.sendall(_r_str.encode())

            

    except Exception as ex:
        print(ex)
        if client_socket is not None:
            _r_str = json.dumps({"r": "err", "msg": str(ex)})
            client_socket.sendall(_r_str.encode())
            # time.sleep(5)
    except KeyboardInterrupt:
        print('ctrl-c interrupt exit')
        time.sleep(1)
        break
    except OSError:
        print(OSError)
        time.sleep(5)
        break
    client_socket.close()

print('server stop')
server_socket.close()
time.sleep(5)
# %%
