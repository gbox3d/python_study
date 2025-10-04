
#참고
#https://wiki.python.org/moin/UdpCommunication
#https://python.flowdas.com/library/struct.html
#https://m.blog.naver.com/PostView.nhn?blogId=s2kiess&logNo=220243476924&proxyReferer=https:%2F%2Fwww.google.com%2F

#%%
import socket
from struct import *

udp_socket = socket.socket(
    socket.AF_INET, #internet
    socket.SOCK_DGRAM # udp
    )

print('init socket')

#%%
udp_socket.sendto(b"hello", ('localhost', 8284))

# %%

_buf = pack('<LBBhf',99,21,0,257,3.14)
print(_buf)
_sendbytenum = udp_socket.sendto(_buf, ('localhost', 8284))
print(f'{_sendbytenum} bytes sned')

try :
    udp_socket.settimeout(3.0)
    _data,_rinfo = udp_socket.recvfrom(1024)
    print(f'recv data ip : {_rinfo[0]} port : {_rinfo[1]}')
    # print(len(_data))
    _res = unpack(b'<LBBHH',_data)
    print(_res)
except Exception as ex: 
    print('에러가 발생 했습니다', ex) 





# %%
