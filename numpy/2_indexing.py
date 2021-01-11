
#%% load module
#init module
import numpy as np 
print('numpy ready')

#%%
# 1차원 예제
arr1 = np.arange(0,10,1) # 0~9 배열만들기 

#첫번째요소
print(arr1[0])
# out : 0

#3번째 요소 
print(arr1[3])
# out : 3

# 0~3번째 요소 
print(arr1[0:3])
print(arr1[:3])

# 전체 
print(arr1[:])


#%%
# 2차원 
arr2 = np.array([[1,2,3,4],
                 [5,6,7,8],
                 [9,10,11,12]])

print(arr2)

print(arr2[1,0]) # arr2[1][0] 와 같다.
print(f'arr2[1,2] : {arr2[1,2]}')

#2행의 모든 원소꺼내기 
print(arr2[2,:])

#2열의 모든 원소 꺼내기 
print(arr2[:,2])

# 0,1열의 모든 원소 꺼내기 
print(arr2[:,0:2])

#%% 3차원 
x2 = np.array([
    [[1,2,9]],
    [[3,4,10]],
    [[5,6,11]],
    [[7,8,12]]
    ])

print(type(x2))
# print(x2)

print('x2[0] => ' , x2[0]) # 첫번째 배열 원소
print('x2[0,0] => ' , x2[0,0])
print('x2[0,0] => ' , x2[1,0])
print('x2[0,0] => ' , x2[2,0])

print('x2[1,:,:] =>', x2[1,:,:]) # x2[1] 와 같은 결과 

# print('x2[:,0] => ', x2[:,0])  # 가로 꺼내기 
# print(x2[ : ])

print(x2[:,:,0]) # 1번째 열 원소 만 꺼내기
print(x2[:,:,1]) # 2번째 열 원소 만 꺼내기 


print('_________')





# %% 연산 예제

_a = np.array([1,2,3])
_b = np.array([4,5,6])

_c = _a * _b
print(_c)



# %%
