#%%
import numpy as np
array_data = np.arange(1,10,1)

#%%
mask1 = np.array([True, False, True, False, True, False, True, False, True])
masked = array_data[mask1] #filtering
print(masked)
# %%
mask2 = array_data % 2 == 0 # make evennumber mask
masked = array_data[mask2] # filtering
print(masked)
# %%
print( array_data[ array_data > 2 ]) # compare two mask
#%%
array2 = np.arange(1,10,1).reshape(3,3)
print(array2)
#%%
# 두번째 숫자가 5인 것만 고르기 
print(array2[array2[:,1] == 5]) # filter by column

_array2 = np.array([ i + np.array([0,1,0]) for i in array2[array2[:,1] == 5]])

print(_array2)
    
    
# print(array2)

# %%
