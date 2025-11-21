#%%
import torch
import matplotlib.pyplot as plt

# 1) 입력 범위 설정 (-10 ~ 10)
x = torch.linspace(-10, 10, steps=400)

# 2) 시그모이드 적용
y = torch.sigmoid(x)

plt.figure(figsize=(10, 5))

# ---- 시그모이드 곡선 ----
plt.subplot(1, 2, 1)
plt.plot(x, y, label="torch.sigmoid(x)")
plt.axhline(0.5, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.title("Sigmoid Function (torch.sigmoid)")
plt.xlabel("x")
plt.ylabel("sigmoid(x)")
plt.grid(alpha=0.3)
plt.legend()



# sigmoid'(x) = sigmoid(x) * (1 - sigmoid(x))
dy = y * (1 - y)
# ---- 기울기 곡선 ----
plt.subplot(1, 2, 2)
plt.plot(x, dy, label="sigmoid'(x)", color="orange")
plt.axvline(0, color='gray', linestyle='--')
plt.title("Sigmoid Derivative (Gradient)")
plt.xlabel("x")
plt.ylabel("gradient")
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
#%%
