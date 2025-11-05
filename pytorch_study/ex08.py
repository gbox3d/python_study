#%%
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# 두 클래스 간의 logit 차이
z = torch.linspace(-5, 5, 200)
# class1 확률 = e^z / (e^z + e^0)
p = torch.exp(z) / (torch.exp(z) + 1)

plt.figure(figsize=(7,4))
plt.plot(z, p, color='blue')
plt.title("Softmax (2-class case → sigmoid function)")
plt.xlabel("logit difference (z1 - z0)")
plt.ylabel("P(class=1)")
plt.grid(True)
plt.show()
# %%
