#%%
import torch
import matplotlib.pyplot as plt

x = torch.linspace(-5, 5, 200)

# Sigmoid
sigmoid_y = torch.sigmoid(x)

# Softmax (2-class 비교)
logits = torch.stack([x, -x], dim=1)  
softmax_y = torch.softmax(logits, dim=1)[:,0]  

plt.figure(figsize=(10,5))

plt.plot(x, sigmoid_y, label="Sigmoid", linewidth=2)
plt.plot(x, softmax_y, label="Softmax(2-class)", linewidth=2)

plt.axhline(0.5, color='gray', linestyle='--')
plt.grid(alpha=0.3)
plt.title("Sigmoid vs Softmax (Decision Curve)")
plt.xlabel("Input x")
plt.ylabel("Probability")
plt.legend()
plt.show()
#%%


# %%
