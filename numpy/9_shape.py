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
