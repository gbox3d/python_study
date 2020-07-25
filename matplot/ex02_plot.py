#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#%%
plt.plot([1,2,3],[5,7,2])
plt.plot([1,2,3],[3,10,7])
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('title')
plt.show

# %%

_data = np.random.rand(10) 
print(_data)

#%%
print(range(10))
plt.xlabel('index')
plt.ylabel('value')
plt.plot(  range(len(_data)),_data)
# plt.show()

# %%
