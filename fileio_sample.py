import pathlib
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

#현제 실행경로 구하기
print("current path (cwd) : ",os.getcwd())
print("current path (pathlib) : ",pathlib.Path().absolute())

filelist = os.listdir()
# print(filelist)
for _file in filelist : 
    print(_file)
