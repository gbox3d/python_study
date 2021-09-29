#%%
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt

#%%
# 0) Prepare data
X_numpy, y_numpy = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=4)

print(X_numpy.shape)
#%%
plt.plot(X_numpy, y_numpy, 'ro')
plt.show()
# %%
