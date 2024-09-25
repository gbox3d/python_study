#참고
# https://rfriend.tistory.com/473

#%%
import numpy as np

# x = np.array([24, 2, 16, 5, 71, 13, 0])

#%%
x = np.random.randint(0,100,10)
print("original : " , x)
print("sort : " , np.sort(x))

#%%

print(np.argsort(x)) # 소팅된 인덱스 구하기
print(x[np.argsort(x)])
print(np.argsort(-x)) #역순 정렬


print('최대값 : ' , x[x.argmax()])
print('최소값 : ' , x[x.argmin()])

#%%
print('2d sort')
x1 = np.array([
    [1,9],
    [0,8],
    [6,3],
    [3,4],
    [4,1]
])

print(x1)
#첫번째 열을 일차원 배열로 만들기

print(x1[:,0])
# 첫번째 열기준 정렬
print("sort index : " , x1[:,0].argsort())

#%%
sort_indices = x1[:,0].argsort()
print( x1[:,0][sort_indices] )

#%%
# 2번째 열기준 정렬
print(x1[x1[:,1].argsort()])


#%%
print('3d sort')
x2 = np.array([
    [[102,131]],
    [[101,237]],
    [[248,236]],
    [[245,135]]
    ])

#%%
print(x2[:,0,0]) # 첫번째 열만 가지고 일차원 배열로 꺼내기

#%%
print( x2[np.argsort(x2[:,0,0])] ) #첫번째 열기준으로 정렬
print( x2[np.argsort(x2[:,0,1])] ) #2번째 열기준으로 정렬


# %%
