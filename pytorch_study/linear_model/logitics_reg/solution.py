"""
빅데이터 분석 기말 실습시험 - 모범답안 예시
주제: 건강검진 데이터로 충치 여부(dental caries) 이진분류 (PyTorch MLP)

사용 데이터:
 - train_dataset.csv : 학습용 데이터
 - test_dataset.csv  : 평가용 데이터

핵심 내용:
 1) Pandas로 CSV 읽기
 2) MinMaxScaler로 입력(X) 정규화
 3) PyTorch MLP 이진 분류 모델 정의
 4) BCE Loss + Adam으로 학습
 5) Train / Test 정확도 측정
"""
#%%
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

# ==========================================
# 0. 환경 설정
# ==========================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device: {DEVICE}")

# 재현성을 위해 시드 고정
torch.manual_seed(42)
np.random.seed(42)

TRAIN_FILE = "train_dataset.csv"
TEST_FILE = "test_dataset.csv"

# ==========================================
# 1. 데이터 로딩
# ==========================================
train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

print("=== Train head ===")
print(train_df.head(), "\n")
print("=== Test head ===")
print(test_df.head(), "\n")

#%%

# ==========================================
# 2. Feature / Target 분리
#    - 타겟: dental caries (0/1)
#    - 입력: 나머지 모든 컬럼
# ==========================================
target_col = "dental caries"

# train/test 공통 컬럼만 사용
common_cols = train_df.columns.intersection(test_df.columns) # 결측치 제거
feature_cols = [col for col in common_cols if col != target_col]
X_train_pd = train_df[feature_cols]
y_train_pd = train_df[[target_col]]  # (N, 1) 형태 유지

X_test_pd = test_df[feature_cols]
y_test_pd = test_df[[target_col]]

print(f"Feature columns ({len(feature_cols)}개):")
print(feature_cols, "\n")

#%%
# ==========================================
# 3. MinMaxScaler 로 정규화 (입력 X만)
#    - 스케일러는 train에만 fit
#    - test에는 transform만 적용
# ==========================================
scaler_X = MinMaxScaler()

X_train_scaled_np = scaler_X.fit_transform(X_train_pd.values)
X_test_scaled_np = scaler_X.transform(X_test_pd.values)

# 타겟 y는 0/1 이므로 스케일링하지 않음
y_train_np = y_train_pd.values.astype(np.float32)  # (N,1)
y_test_np = y_test_pd.values.astype(np.float32)

# ==========================================
# 4. PyTorch Tensor 변환 & 장치 이동
# ==========================================
X_train = torch.tensor(X_train_scaled_np, dtype=torch.float32, device=DEVICE)
y_train = torch.tensor(y_train_np, dtype=torch.float32, device=DEVICE)

X_test = torch.tensor(X_test_scaled_np, dtype=torch.float32, device=DEVICE)
y_test = torch.tensor(y_test_np, dtype=torch.float32, device=DEVICE)

print("X_train shape:", X_train.shape)  # (N, D)
print("y_train shape:", y_train.shape)  # (N, 1)
print("X_test  shape:", X_test.shape)
print("y_test  shape:", y_test.shape, "\n")

#%%
# ==========================================
# 5. MLP 이진분류 모델 정의
#    입력: feature 개수
#    출력: 1 (Sigmoid -> 0~1 확률)
# ==========================================
class MLPBinaryClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid(),  # 출력: 0~1
        )

    def forward(self, x):
        return self.net(x)

input_dim = X_train.shape[1]
model = MLPBinaryClassifier(input_dim).to(DEVICE)

print("=== Model ===")
print(model, "\n")

#%%
# ==========================================
# 6. 손실 함수 & 옵티마이저 설정
# ==========================================
criterion = nn.BCELoss()          # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 500  # 시험용이면 30~100 사이 적당

# ==========================================
# 7. 학습 함수 / 평가 함수
# ==========================================
def compute_accuracy(y_pred_prob, y_true):
    """
    y_pred_prob: (N,1) Sigmoid 출력 (0~1)
    y_true     : (N,1) 0 또는 1
    """
    y_pred_label = (y_pred_prob >= 0.5).float()
    correct = (y_pred_label == y_true).float().sum().item()
    total = y_true.shape[0]
    return correct / total


#%%
# ==========================================
# 8. 학습 루프
# ==========================================
loss_history = []

for epoch in range(1, num_epochs + 1):
    model.train()

    # Forward
    y_pred = model(X_train)           # (N,1)
    loss = criterion(y_pred, y_train)

    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    loss_history.append(loss.item())

    # Epoch별 로그 출력 (10 에폭마다)
    if epoch % 10 == 0 or epoch == 1:
        acc = compute_accuracy(y_pred, y_train)
        print(f"[Epoch {epoch:3d}] Loss = {loss.item():.4f}, "
              f"Train Acc = {acc*100:.2f}%")

print("\n=== 학습 종료 ===\n")

# ==========================================
# 9. Train / Test 정확도 평가
# ==========================================
model.eval()

with torch.no_grad():
    # Train 성능
    train_pred = model(X_train)
    train_acc = compute_accuracy(train_pred, y_train)

    # Test 성능
    test_pred = model(X_test)
    test_acc = compute_accuracy(test_pred, y_test)

print(f"Train Accuracy: {train_acc*100:.2f}%")
print(f"Test  Accuracy: {test_acc*100:.2f}%")


# ==========================================
# 10. (선택) Loss 변화 그래프
#      - 실습시험에서 그래프까지 요구하시면 사용
# ==========================================

plt.figure(figsize=(8, 5))
plt.plot(loss_history)
plt.xlabel("Epoch")
plt.ylabel("Loss (BCE)")
plt.title("Training Loss Curve")
plt.grid(True)
plt.show()

# %%
