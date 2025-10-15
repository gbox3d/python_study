#%%
import numpy as np
array_data = np.arange(1,10,1)

#%%
print(array_data)
mask1 = np.array([True, False, True, False, True, False, True, False, True])
masked = array_data[mask1] #filtering
print(masked)
# %%
mask2 = array_data % 2 == 0 # make evennumber mask
masked = array_data[mask2] # filtering
print(masked)
# %%
array_data = np.random.randint(1,100,10)
print(array_data)
print( array_data[ array_data < 47 ]) # compare two mask
#%%
array_data = np.random.randint(1,100,30).reshape(6,5)
print(array_data)
#%%
# 두번째 숫자가 20보다 작은 행만 출력
print(array_data[array_data[:,1] < 20]) # filter by column
