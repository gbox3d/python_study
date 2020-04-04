for i in range(-5,5) : print(i)

_list = [1,2,3,"hello"]

for item in _list : print(item)

#배열만들기 [표현식 forin 조건문]
_arrfor = [ 10*x for x in range(1,10) if x%2 ]
#홀수레 10을 곱한배열
print(_arrfor)

#for zip
for x,y,z in zip(['a','b','c'],[7,8,9],["hello","hi","one"]) :
    print(x,y,z)