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
    data = client_socket.recv(1024)
    print(f"recevied : {addr} {data.decode()}")

    _str = 'HTTP/1.1 200 OK\r\n'
    _str += 'Content-Type: text/html\r\n\r\n'
    _str += '<!DOCTYPE HTML>\r\n'
    _str += '<html>\r\n<h1>Hello http</h1></html>\n'
    
    client_socket.sendall(_str.encode())




    client_socket.close()

# %%
