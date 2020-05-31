try:
    list = []
    print(list[0])  
#에러가 먼지 모를때
except Exception as ex: 
    print('에러가 발생 했습니다', ex) 


#강제로 예외를 발생 시킬때는 raise를 사용한다.
try:
    raise IOError
except IOError:
    print("강제로 발생된 ioerror")

answer = input("yes or no :")

try: 
    if answer == "yes" : raise Exception
except Exception: print("opps! rase exception")
else : print("ok without exception")
finally : print("finally go throu")
    