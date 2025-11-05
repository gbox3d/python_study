# %%
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

# 2개 클래스 (0, 1)
# 로짓 z = [z0, z1]
z = torch.linspace(-5, 5, 200).unsqueeze(1)  # shape (200, 1)
logits = torch.cat([-z, z], dim=1)  # [ [ -z, z ] ] → class 0 vs class 1

# softmax 확률
probs = F.softmax(logits, dim=1)
p_class1 = probs[:, 1].detach().numpy()

# 실제 정답: class1 = 1
target = torch.ones(200, dtype=torch.long)
loss = F.cross_entropy(logits, target)
loss_values = []
for i in range(len(z)):
    loss_i = F.cross_entropy(logits[i].unsqueeze(0), target[i].unsqueeze(0))
    loss_values.append(loss_i.item())

# 시각화
fig, ax1 = plt.subplots(figsize=(8,5))
ax2 = ax1.twinx()

ax1.plot(z, p_class1, color='blue', label='Softmax Output (P(class=1))')
ax2.plot(z, loss_values, color='red', label='CrossEntropy Loss', linestyle='--')

ax1.set_xlabel("Logit difference (z1 - z0)")
ax1.set_ylabel("Softmax Probability", color='blue')
ax2.set_ylabel("CrossEntropy Loss", color='red')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid(True)
plt.title("Softmax Output vs CrossEntropy Loss")
plt.show()

# %%
