#%%
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

#%% 
# 두 클래스 간의 logit 차이
z = torch.linspace(-5, 5, 200)
# class1 확률 = e^z / (e^z + e^0)
p = torch.exp(z) / (torch.exp(z) + 0.5)

plt.figure(figsize=(7,4))
plt.plot(z, p, color='blue')
plt.title("Softmax (2-class case → sigmoid function)")
plt.xlabel("logit difference (z1 - z0)")
plt.ylabel("P(class=1)")
plt.grid(True)
plt.show()
# %% softmax 함수로 시그모이드 구현
z = torch.linspace(-5, 5, 200) # shape (200,)
z = z.unsqueeze(1)  # shape (200, 1)

logits = torch.cat([-z, z], dim=1)  # [ [ -z, z ] ] → class 0 vs class 1
probs = F.softmax(logits, dim=1)
p = probs[:, 1].detach().numpy()

plt.figure(figsize=(7,4))
plt.plot(z, p, color='blue')
plt.title("Softmax (2-class case → sigmoid function)")
plt.xlabel("logit difference (z1 - z0)")
plt.ylabel("P(class=1)")
plt.grid(True)
plt.show()


# %%
