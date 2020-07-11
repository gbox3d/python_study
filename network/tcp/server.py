import socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind("",8282)
server_socket.listen(5) # 5 CONNECTION QUEUE

client_socket ,addr = server_socket.accept()
data = client_socket.recv(1024)

print("recevied :" ,addr, data.decode())

client_socket.close()
