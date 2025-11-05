# %%
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

# 2D 입력 공간 정의
x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
xx, yy = np.meshgrid(x, y)

# 각 점을 [x, y]로 묶어 (N, 2)
inputs = np.c_[xx.ravel(), yy.ravel()]
inputs_torch = torch.tensor(inputs, dtype=torch.float32)

# 3개 클래스에 대한 임의의 weight (3x2) 와 bias (3)
W = torch.tensor([[1.0, 0.5],
                  [-1.0, 0.8],
                  [0.5, -1.2]], dtype=torch.float32)
b = torch.tensor([0.0, -0.5, 0.8])

# logits 계산: z = XWᵀ + b
logits = inputs_torch @ W.T + b

# softmax 확률 (각 클래스별)
probs = F.softmax(logits, dim=1).detach().numpy()

# 클래스별 확률 분리
p1 = probs[:, 0].reshape(xx.shape)
p2 = probs[:, 1].reshape(xx.shape)
p3 = probs[:, 2].reshape(xx.shape)

# 확률이 가장 큰 클래스를 색상으로 표현
pred_class = np.argmax(probs, axis=1).reshape(xx.shape)

# -----------------------------
# 시각화
# -----------------------------
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, pred_class, alpha=0.3, levels=[-0.5,0.5,1.5,2.5],
             colors=["#FFAAAA","#AAFFAA","#AAAAFF"])
plt.contour(xx, yy, p1, levels=[0.33,0.5,0.66], colors="r", linestyles="dashed", linewidths=1)
plt.contour(xx, yy, p2, levels=[0.33,0.5,0.66], colors="g", linestyles="dashed", linewidths=1)
plt.contour(xx, yy, p3, levels=[0.33,0.5,0.66], colors="b", linestyles="dashed", linewidths=1)

plt.title("3-Class Softmax Decision Regions (Contour of Probabilities)")
plt.xlabel("x₁ (feature 1)")
plt.ylabel("x₂ (feature 2)")
plt.grid(True)
plt.show()

# %%
