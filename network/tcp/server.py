#%%
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1",8282))
server_socket.listen(5) # 5 CONNECTION QUEUE

print('wait connect')
client_socket ,addr = server_socket.accept()
print(f'client connected {addr}')

print('wait data')
data = client_socket.recv(1024)
print(f"recevied : {addr} {data.decode()}")

client_socket.close()

# %%
