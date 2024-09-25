# %%
import sys
import numpy as np 
print(sys.version)
# %%
_ary = np.array(range(12))

print(_ary.shape)
# %% 특정축기준으로 차원늘리기
_ary2 = np.expand_dims(_ary,axis=0) #첫번째 축
print(_ary2.shape)
print(_ary2)

#%%
__ary2 = np.reshape(_ary,(1,12)) # 위의 예와 똑같다.
print(__ary2.shape)
print(__ary2)

_ary3 = np.expand_dims(_ary,axis=1) # 두번째축 
print(_ary3.shape)
print(_ary3)

#%% 차원 변환 
_ary4 = np.reshape(_ary,(2,6))
print(_ary4.shape)
print(_ary4)
# %%
_ary5 = np.reshape(_ary,(2,2,3))
print(_ary5.shape)
print(_ary5)
#%%
_ary6 = np.reshape(_ary,(6,2,1))
print(_ary6.shape)
print(_ary6)
# %%
_ary7 = [1,2,3,4,5,6,7,8,9,10]
_temp = np.reshape(_ary7,(-1,2)) # 두개씩 묶기 
px = list(_temp[:,0] ) # x 좌표
py = list(_temp[:,1] ) # y 좌표
print( px )
print(type(px))
print(type(_ary7))
print(type(_temp[:,0]))
# %%

#%% 인덱스 정렬 n,5 차원 데이터 정렬
x = np.array([91,145,142,175,59,1,2,3,4,5 ])

#%% 5개씩 묶어서 한차원 높이기 
_x = x.reshape(-1,5)
print(_x)

# %%
__x = _x[:,0]
# %%
sortidx =  __x.argsort()
# %%
__sort_x = [ _x[i] for i in sortidx]
print(__sort_x)
# %%
