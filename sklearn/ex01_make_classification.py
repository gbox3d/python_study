#%%
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')

from sklearn.datasets import make_classification
#%%
nSamples = 1000
X,y = make_classification(
    n_samples=nSamples,n_features=2,n_informative=2,
    n_redundant=0,n_clusters_per_class=1
)

print(X.shape)
print(y.shape)
#%%
print(X[0])
print(X[0,0])
print(X[0,1])
# %%

fig,ax=plt.subplots(1,1,figsize=(10,6))
ax.grid()
ax.set_xlabel('X')
ax.set_ylabel('y')

for i in range(nSamples) :
    _x0 = X[i,0]
    _x1 = X[i,1]
    color = 'b'
    if y[i] == 0 :
        color = 'r'
    
    ax.scatter(_x0,_x1,edgecolors='k',alpha=0.5,marker='o',color=color)

plt.show()


# %%
