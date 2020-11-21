#%%
import pathlib
import os

#%%
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

#%%
#with 로 close 자동화 
#fd = open() 과 같고 with를 벚어날때 자동으로 close
with open('test.txt') as fd:
    print(fd.read())

#%%
#현제 실행경로 구하기
print("current path (cwd) : ",os.getcwd())
print("current path (pathlib) : ",pathlib.Path().absolute())

#%%
#파일 리스팅 
filelist = os.listdir()
# print(filelist)
for _file in filelist : 
    print(_file)

#%%
import struct
fd = open('test.bin',"wb")
buf = bytes("hello python",'utf-8')

fd.write(struct.pack('I',len(buf)))
fd.write(buf)
fd.close()
# %%
