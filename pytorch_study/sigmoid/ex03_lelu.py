#%%
import torch
import matplotlib.pyplot as plt

# 입력 범위 (-10 ~ 10)
x = torch.linspace(-10, 10, steps=400)

# Sigmoid
sig = torch.sigmoid(x)
sig_grad = sig * (1 - sig)  # derivative

# ReLU
relu = torch.relu(x)
relu_grad = torch.where(x > 0, torch.ones_like(x), torch.zeros_like(x))

# ---- 그래프 그리기 ----
plt.figure(figsize=(12, 8))

# 1) Sigmoid 함수
plt.subplot(2, 2, 1)
plt.plot(x, sig, label="Sigmoid", color='blue')
plt.title("Sigmoid Function")
plt.grid(alpha=0.3)
plt.legend()

# 2) Sigmoid 기울기
plt.subplot(2, 2, 2)
plt.plot(x, sig_grad, label="Sigmoid Derivative", color='cyan')
plt.title("Sigmoid Gradient (Vanishing)")
plt.grid(alpha=0.3)
plt.legend()

# 3) ReLU 함수
plt.subplot(2, 2, 3)
plt.plot(x, relu, label="ReLU", color='red')
plt.title("ReLU Function")
plt.grid(alpha=0.3)
plt.legend()

# 4) ReLU 기울기
plt.subplot(2, 2, 4)
plt.plot(x, relu_grad, label="ReLU Gradient", color='orange')
plt.title("ReLU Gradient (Constant for x>0)")
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
#%%
