
#%%
import socket
from struct import *

udp_socket = socket.socket(
    socket.AF_INET, #internet
    socket.SOCK_DGRAM # udp
    )
udp_socket.bind(('',8284))

print('init socket')

while True:
    _data, _rinfo = udp_socket.recvfrom(1024) # buffer size is 1024 bytes
    _packet = unpack("<LBBhf",_data)
    print(_packet)
    if _packet[0] == 99 :
        _res = pack('<LBBHH',77,0,9,300,400)
        udp_socket.sendto(_res,(_rinfo[0],_rinfo[1]))
    else :
        _res = pack('<LBBHH',77,0,0,0,0)
    

# %%
