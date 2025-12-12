"""
빅데이터 분석 기말 실습 - 정답 코드 (PyTorch MLP 이진 분류)

데이터: pass_dataset.csv
목표: 공부시간/출석률/수면/스트레스 정도로 합격 여부(pass)를 예측

컬럼:
- study_time     : 하루 평균 공부 시간
- attendance     : 출석률 (%)
- sleep_hours    : 하루 수면 시간
- stress_level   : 스트레스 지수
- pass           : 0(불합격), 1(합격)  ← 타겟
"""

#%%
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# =========================================
# 0. 환경 설정
# =========================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("[INFO] Using device:", DEVICE)

torch.manual_seed(42)
np.random.seed(42)

FILE_NAME = "pass_dataset.csv"
TARGET = "pass"

# =========================================
# 1. 데이터 로딩
# =========================================
df = pd.read_csv(FILE_NAME)
print("데이터 크기:", df.shape)
print(df.head(), "\n")

# =========================================
# 2. Feature / Target 분리
# =========================================
feature_cols = ["study_time", "attendance", "sleep_hours", "stress_level"]

X_pd = df[feature_cols]
y_pd = df[[TARGET]]   # (N, 1) 형태 유지

# =========================================
# 3. Train / Test 분할
# =========================================
X_train_pd, X_test_pd, y_train_pd, y_test_pd = train_test_split(
    X_pd, y_pd, test_size=0.2, random_state=42, stratify=y_pd
)

print("Train 크기:", X_train_pd.shape, y_train_pd.shape)
print("Test  크기:", X_test_pd.shape, y_test_pd.shape, "\n")

# =========================================
# 4. MinMaxScaler 정규화 (입력 X만)
# =========================================
scaler = MinMaxScaler()

X_train_np = scaler.fit_transform(X_train_pd.values)
X_test_np = scaler.transform(X_test_pd.values)

y_train_np = y_train_pd.values.astype(np.float32)
y_test_np = y_test_pd.values.astype(np.float32)

# =========================================
# 5. PyTorch Tensor 변환
# =========================================
X_train = torch.tensor(X_train_np, dtype=torch.float32, device=DEVICE)
y_train = torch.tensor(y_train_np, dtype=torch.float32, device=DEVICE)

X_test = torch.tensor(X_test_np, dtype=torch.float32, device=DEVICE)
y_test = torch.tensor(y_test_np, dtype=torch.float32, device=DEVICE)

print("X_train:", X_train.shape, "y_train:", y_train.shape)
print("X_test :", X_test.shape, "y_test :", y_test.shape, "\n")

#%%
# =========================================
# 6. MLP 모델 정의
# =========================================
class PassMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid(),  # 0~1 확률 출력
        )

    def forward(self, x):
        return self.net(x)

input_dim = len(feature_cols)
model = PassMLP(input_dim).to(DEVICE)
print(model, "\n")

# =========================================
# 7. 손실함수 / 옵티마이저
# =========================================
criterion = nn.BCELoss()   # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

# =========================================
# 8. 정확도 계산 함수
# =========================================
def accuracy(y_prob, y_true):
    """ 
    y_prob : (N,1) Sigmoid 결과 (0~1)
    y_true : (N,1) 라벨 (0 또는 1)
    """
    y_label = (y_prob >= 0.5).float()
    correct = (y_label == y_true).float().sum().item()
    return correct / y_true.shape[0]

# =========================================
# 9. 학습 루프
# =========================================
epochs = 500
loss_history = []

for epoch in range(1, epochs + 1):
    model.train()

    y_pred = model(X_train)             # (N,1)
    loss = criterion(y_pred, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    loss_history.append(loss.item())

    if epoch % 10 == 0 or epoch == 1:
        train_acc = accuracy(y_pred, y_train)
        print(f"[Epoch {epoch:3d}] Loss={loss.item():.4f}, "
              f"Train Acc={train_acc*100:.2f}%")

print("\n=== 학습 완료 ===\n")

# =========================================
# 10. Train / Test 성능 평가
# =========================================
model.eval()
with torch.no_grad():
    train_pred = model(X_train)
    test_pred = model(X_test)

train_acc = accuracy(train_pred, y_train)
test_acc = accuracy(test_pred, y_test)

print(f"최종 Train Accuracy: {train_acc*100:.2f}%")
print(f"최종 Test  Accuracy: {test_acc*100:.2f}%")

# =========================================
# 11. Loss 변화 그래프
# =========================================
plt.figure(figsize=(8,5))
plt.plot(loss_history)
plt.xlabel("Epoch")
plt.ylabel("Loss (BCE)")
plt.title("Training Loss Curve (pass_dataset)")
plt.grid(True)
plt.show()
# %%