# %%
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# ------------------------------
# 0) 데이터 준비
# ------------------------------
X = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
Y = torch.tensor([2, 4, 6, 8], dtype=torch.float32)

# ------------------------------
# 1) forward 함수 정의 (교수님 버전)
# ------------------------------
def forward(x, w):
    return w * x

# ------------------------------
# 2) 학습 함수 (옵티마이저별)
# ------------------------------
def train_with_optimizer(optimizer_name, learning_rate=0.01, n_iters=100):
    # 가중치 초기화
    w = torch.tensor(0.0, dtype=torch.float32, requires_grad=True)
    loss_fn = nn.MSELoss()

    # 옵티마이저 선택
    if optimizer_name == "sgd":
        optimizer = torch.optim.SGD([w], lr=learning_rate)
    elif optimizer_name == "momentum":
        optimizer = torch.optim.SGD([w], lr=learning_rate, momentum=0.9)
    elif optimizer_name == "adam":
        optimizer = torch.optim.Adam([w], lr=learning_rate)
    else:
        raise ValueError("unknown optimizer")

    losses = []

    # ------------------------------
    # 3) 학습 루프
    # ------------------------------
    for epoch in range(n_iters):
        # forward pass
        y_pred = forward(X, w)

        # loss 계산
        loss = loss_fn(Y, y_pred)

        # backward pass
        optimizer.zero_grad()
        loss.backward()

        # update
        optimizer.step()

        losses.append(loss.item())

    return w.item(), losses

#%%
# ------------------------------
# 4) 세 가지 옵티마이저로 학습
# ------------------------------
results = {}
for name in ["sgd", "momentum", "adam"]:
    final_w, losses = train_with_optimizer(name, learning_rate=0.01, n_iters=100)
    results[name] = (final_w, losses)
    print(f"{name.upper()} 최종 w = {final_w:.4f}, f(5) = {forward(5, torch.tensor(final_w)).item():.3f}")

#%%
# ------------------------------
# 5) 시각화
# ------------------------------
plt.figure(figsize=(8,5))
for name, (_, losses) in results.items():
    plt.plot(losses, label=name)

plt.title("Optimizer Comparison (SGD vs Momentum vs Adam)")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.legend()
plt.grid(True)
plt.show()

# %%
