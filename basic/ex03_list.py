# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# list 선언하기

# %% tuple
_tuple = (1,2,3,4,5)
print(_tuple)
print(type(_tuple))

#%% unpacking
a,b,c,d,e = _tuple
print(a,b,c,d,e)



# %% tuple 은 수정 불가능하다.
# _list[1] = 0
print(_tuple[1])


# %%
for v in _tuple :
    print(v)

# %%

_list = [ v for v in _tuple]
print(_list)
# %%
# 리스트 덧씌우기
__list = [_list]
print(__list)
# %%
__list[0][2] = 20
print(__list)
# %%

px = [1,2,3,4,5]
py = [6,7,8,9,10]
poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
print(poly)
poly = [p for x in poly for p in x] # flatten
print(poly)

# %%

#%% container type unpacking

numbers = [1,2,3,4,5,6]

*a, = numbers # _a -> [1,2,3,4,5,6]
print(a) # _a [1,2,3,4,5,6] 

*a,b = numbers
print(a) # _a -> [1,2,3,4,5] ,_b -> 6
print(b) # 6

_,*b,_,_ = numbers
print(b) # b -> [2,3,4]

# %%
print( [1,] + [2,])
print( (1,) + (2,))

# %% for loop, numbers
numbers = [1,2,3,4,5,6]
for i in numbers:
    print(i)

for i in range(6):
    print(numbers[i])
# %% for loop, enumerate
for i, v in enumerate(numbers):
    print(i,v)

# %% insert 
numbers.insert(3,66)
print(numbers)


# %% append
numbers.append(77)
print(numbers)

# %%
numbers = [1,2,3,4,5,6]
numbers.extend([7,8,9])
print(numbers)

# %%
numbers = [1,2,3,4,5,6]
numbers += [7,8,9]
print(numbers)
# %%
# remove
numbers.remove(3)
print(numbers)
# %%
# pop
numbers = [1,2,3,4,5,6]
numbers.pop()
print(numbers)
# %%
numbers = [1,2,3,4,5,6]
numbers.pop(0)
print(numbers)
# %%
numbers = [1,2,3,4,5,6]
numbers.clear()
print(numbers)

# %%
#push
numbers = [1,2,3,4,5,6]
numbers.append(7)
print(numbers)
# %%
# stack
numbers = [1,2,3,4,5,6]
numbers.append(7)
print(numbers)
print(numbers.pop())
print(numbers)

# %%
# queue
numbers = [1,2,3,4,5,6]
numbers.append(7)
print(numbers)
print(numbers.pop(0))
print(numbers)
# %%
# list comprehension
numbers = [1,2,3,4,5,6]
numbers = [i+1 for i in numbers]
print(numbers)
# %% sort
numbers = [1,5,2,4,3,6]
numbers.sort()
print(numbers)

# %%
tensor = [[1,2,3],[4,5,6],[7,8,9]]
print(tensor)
#%%차원을 하나 줄인다.
tensor = [v for t in tensor for v in t]
print(tensor)

# %%
_random_list = [i for i in range(10)]
#shurffle
import random
random.shuffle(_random_list)

print(_random_list)
# %%
