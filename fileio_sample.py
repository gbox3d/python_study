import os

filename = "test.txt"
if os.path.isfile("test.txt") :
    print('file exist')
    fd = open(filename,"r")
    data = fd.read()
    print(data)
    fd.close()
else : 
    print('create file')
    fd = open(filename,"w")
    fd.write("hello python")
    fd.close()


