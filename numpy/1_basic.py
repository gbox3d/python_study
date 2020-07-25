# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import sys
import numpy as np 

print(sys.version)
data1 = [1,2,3,4,5]
print(data1,type(data1))

# %% [markdown]
# ### 기본 정보 얻기
# 
# dtype : 데이터 타입구하기  
# shape : 데이터 구성 형식
# 

# %%

arr1 = np.array(data1)

# print(np.shape(arr1))
print( f'array length use shape value  {arr1.shape[0]} ')
print( f'array length use len {len(arr1)} ')

print(arr1,type(arr1))
print(f'data type : {arr1.dtype}')

# %% [markdown]
# ### 데이터 형 변환
# astype()  

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

# %% [markdown]
# ### masking
# ```
# array[조건식] = 마스킹값 
# ```

# %%
#2보다 큰것만 True
print(_ary3 > 2)
print(_ary4[_ary3 > 2])


# %%

_ary5 = np.array([20,21,22,23])
_ary6 = np.array(['a','b','c','d'])
_ary6[_ary3 > 2] = '-'

print(_ary6)

# %% [markdown]
# ### copy
# 

# %%
_a1 = np.array([1,2,3,4,5,6,7,8,9])
_a2 = np.array([10,11,12,13,14,15,16,17,18,19])

print(_a1)
_a1[2:5] = _a2[3:6]
print(_a1)


