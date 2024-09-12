#초기화 예제
#%%
import numpy as np
# import matplotlib.pyplot as plt

#%%
arr2 = np.zeros(10)
print(arr2)
arr3 = np.zeros(10,dtype=np.uint8)
print(arr3)



#%%
print(np.ones(10))

print(np.ones(10,dtype=np.uint32))
# print(np.ones((3,2),dtype=np.int))

#%%
#0~10까지 1씩 증가하는 배열 만들기
print(np.arange(0,10,1))

#%%
# 2x3 의 2차원 배열 만들기
print(np.arange(6).reshape(2,3))

# %%
# 원소수가 10개인 1차월 랜덤 배열  만들기
print (np.random.rand(10))

# %%
#램덤 2차원배열만들기 
_rand_array = np.random.rand(6,4) * 100
_rand_array = _rand_array.astype(np.int32)
print(_rand_array)

# %%
