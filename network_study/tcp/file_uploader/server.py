#%%

import socket               # Import socket module


import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display

import io
import json

try:
    s = socket.socket()         # Create a socket object
    # host = socket.gethostname() # Get local machine name
    port = 8181                 # Reserve a port for your service.
    s.bind(("", port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    print(f'start upload server  : {port}')
    while True:
        print('wait conn...')
        c, addr = s.accept()     # Establish connection with client.
        print ('Got connection from', addr)
        print ("Receiving...")

        header = c.recv(1024)
        print(header.decode())

        header = json.loads(header.decode())
        
        fn = header["fn"]
        print("threshold : " + str(header['th']))
        f = open(f'./uploads/{fn}','wb')

        _data = bytes()
        # l = c.recv(1024)
        while True:
            l = c.recv(1024)
            if l == b'' : break; #Fin 을 받으면..

            print ("Receiving...",_data.__sizeof__(),l.__sizeof__())
            f.write(l)
            _data += l

        # f.write(_data)
        f.close()

        #이미지 보기 
        _img = Image.open(io.BytesIO(_data)) 
        display(_img)
        
        print ("Done Receiving")
        c.send('done\r\n\r\n'.encode())
        c.close()                # Close the connection
        
except Exception as ex:
    print(ex)
except KeyboardInterrupt as kbi:
    print(kbi)


# %%
