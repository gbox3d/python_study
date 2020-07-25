#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#%%
_data1 = np.random.rand(100)
_data2 = np.random.rand(100)

#%%

plt.subplot(1,2,1)
plt.title('data 1')
plt.plot(range(100),_data1)

plt.subplot(1,2,2)
plt.title('data 2')
plt.plot(range(100),_data2)
plt.show()

# %%
