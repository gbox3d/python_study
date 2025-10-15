#%%
import numpy as np 

#%%
gate_data = np.loadtxt('./gate.csv', delimiter=',', dtype=np.float32, skiprows=1)

print(gate_data)


# %%
X = gate_data[ : ,0:2]
print(X)
# %%
Y_AND = gate_data[:,2]
print(Y_AND)
# %%
Y_OR = gate_data[:,3]
print(Y_OR)
#%%
Y_XOR = gate_data[:,4]
print(Y_XOR)
# %%
