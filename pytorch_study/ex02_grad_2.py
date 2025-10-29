# filename: plot_autograd_mean_grad.py
# 목적:
#   z = mean(3*(x+2)^2) 에 대해
#   1) g(t) = 3*(t+2)^2 연속 곡선
#   2) 샘플 점 (x_i, 3*(x_i+2)^2)
#   3) z (평균) 수평선
#   4) 각 점 위에 dz/dx_i 주석
# 를 matplotlib 한 개의 그래프에 표시
#
# 수식:
#   z = (1/n) * sum_i 3*(x_i+2)^2
#   ∂z/∂x_i = (1/n) * 6*(x_i+2) = (6/n)*(x_i+2)

#%%
import torch
import numpy as np
import matplotlib.pyplot as plt

#%%

n=5

x = torch.randn(n, requires_grad=True)

xmin = float(x.min().item()) - 2.5
xmax = float(x.max().item()) + 2.5

print(f"x min: {xmin}, x max: {xmax}")


t = np.linspace(xmin, xmax, 400)
g = 3.0 * (t + 2.0) ** 2
plt.figure(figsize=(10, 5))
plt.plot(t, g, label="g(t) = 3·(t + 2)^2")       # 연속 곡선

#%%
y = x + 2
f_elem = y * y * 3                # element-wise: 3*(x+2)^2
z = f_elem.mean()                 # scalar
z.backward()                      # 채워짐: x.grad = ∂z/∂x

# numpy 변환
x_np = x.detach().numpy()
f_np = f_elem.detach().numpy()
z_scalar = float(z.item())
grad_np = x.grad.detach().numpy()

plt.figure(figsize=(10, 5))
plt.plot(t, g, label="g(t) = 3·(t + 2)^2")       # 연속 곡선
plt.scatter(x_np, f_np, label="samples (x_i, 3·(x_i+2)^2)")  # 샘플 점
plt.axhline(z_scalar, linestyle="--", label=f"mean z = {z_scalar:.4f}")  # 평균선

# 4) 각 점 위에 dz/dx_i 주석
    #    이론값: (6/n)*(x_i+2). PyTorch의 x.grad와 동일해야 함.
for xi, fi, gi in zip(x_np, f_np, grad_np):
    plt.annotate(
        f"dz/dx={gi:.3f}",
        (xi, fi),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=9
    )
plt.show()

# %%
