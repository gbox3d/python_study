# %%
import sys
import numpy as np 

print(sys.version)

#%%
a = np.empty(0)
print(a)
a = np.append(a,1)
print(a)
a = np.append(a,2)
print(a)

# %%
data1 = [1,2,3,4,5]
print(data1,type(data1))

arr1 = np.array(data1)

# print(np.shape(arr1))
print( f'array length use shape value  {arr1.shape[0]} ')
print( f'array length use len {len(arr1)} ')

print(arr1,type(arr1))
print(f'data type : {arr1.dtype}')

#%%
print(arr1[0:2])
print(data1[0:2])

# %%
_arr1 = arr1.astype(np.float)
print(_arr1)
print(_arr1.dtype)
# %%
#배열로 만들기 
_ary3 = np.array([1,2,3,4])
_ary4 = np.array([10,11,12,13])

print( type(_ary3) , type(_ary4) )

print(_ary3[0:4]*2) 
print(_ary4[0:4]*2) # 2 곱하기 

# %% 비교문으로 골라내기 
_ary1 = np.array([1,2,3,4])
_ary2 = _ary1 > 2
#2보다 큰것만 True
print( _ary2 )
print( (_ary2).sum()) # 조건에 맞는 원소 객수 구하기 
#골라내기
print(_ary1[_ary2])

# %%
_arg3 = np.array([1,2,3,4])
_ary6 = np.array(['a','b','c','d'])
_ary6[_ary3 > 2] = '-'
print(_ary6)


# %% 인덱싱 
_a1 = np.array([1,2,3,4,5,6,7,8,9])
_a2 = np.array([10,11,12,13,14,15,16,17,18,19])

print(_a1)
_a1[2:5] = _a2[3:6]
print(_a1)

#%%
a = np.zeros(10)
print(a)

# %%
a = np.zeros((3,) )
print(a)

# %%
a = np.zeros((3,) + (2,2)) # (3,2,2) 형식이 만들어짐 
print(a)
print(a.shape)
# %%
a = np.zeros((3,1)) # (3,1) 형식이 만들어이짐
print(a) 
print(a.shape)
# %%
