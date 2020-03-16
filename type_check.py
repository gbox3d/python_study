a=1
b="hello"

print(type(a))
print(type(b))

#반환결과를 문자로 만들어서 체크
if str(type(b)) == "<class 'str'>" : print("b is str")

if isinstance(type(a),int) == True : print("a is int")

c=3.14
print( type(c) is float )

