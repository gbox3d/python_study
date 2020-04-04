import numpy as np 

#파이썬은 배열이 없다. 배열을 사용하고싶으면 numpy를 사용한다.

#리스트 
_ary1 = [1,2,3,4,5,6,7,8,9]
_ary2 = ['a','b','c','d','e','f']

# _ary1[_ary2 == 1] == 10

print(type(_ary1))

#일부분 전송 
_ary1[6:8] = _ary2[0:2]

print(_ary1)

#배열로 만들기 
_ary3 = np.array([1,2,3,4])
_ary4 = np.array([10,11,12,13])

print(type(_ary3))

print(_ary1[0:4]*2) # 2번 반복 ,리스트형 
print(_ary3[0:4]*2) # 2번 곱하기 

#2보다 큰것만 True
print(_ary3 > 2)

print(_ary4[_ary3 > 2])

_ary4[_ary3 > 2] = 100

print(_ary4)



