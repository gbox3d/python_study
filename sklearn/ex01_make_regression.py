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

X, y = datasets.make_regression(n_samples=100, n_features=2, noise=20, random_state=4)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X[:,0], X[:,1], y, c='red')
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_zlabel("Target")

plt.show()

# %%
