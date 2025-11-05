# %%
import torch, matplotlib.pyplot as plt
import torch.nn as nn

x = torch.linspace(-3, 3, 100)
mse = x**2 # MSELoss
mae = torch.abs(x) # MAELoss
huber = torch.where(torch.abs(x)<1, 0.5*x**2, torch.abs(x)-0.5) # SmoothL1Loss

plt.figure(figsize=(8,5))
plt.plot(x, mse, label="MSELoss (L2)")
plt.plot(x, mae, label="MAELoss (L1)")
plt.plot(x, huber, label="SmoothL1Loss (Huber)")
plt.legend(); plt.grid(True)
plt.title("Regression Loss Functions Comparison")
plt.xlabel("Prediction Error (y - ŷ)")
plt.ylabel("Loss Value")
plt.show()

# %%
