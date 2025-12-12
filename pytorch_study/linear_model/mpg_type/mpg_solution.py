"""
빅데이터 분석 기말 실습 - 모범답안 예시 (PyTorch 신경망 + MinMaxScaler)

데이터: auto_mpg_exam_dataset.csv

실습 목표:
 1) CSV를 Pandas로 읽기
 2) MinMaxScaler로 입력(X), 타겟(y) 정규화
 3) PyTorch 신경망(MLP) 모델 정의 및 학습
 4) Test 셋에 대해 RMSE, MAE, R^2 계산
 5) 임의 차량 1대의 mpg 예측
"""
#%%
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# 0. 환경 설정
# -----------------------------
# 4070 환경: GPU 사용 가능하면 자동으로 cuda 사용
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device: {DEVICE}")

torch.manual_seed(42) # 랜덤 시드 고정 (재현성 위해)

FILE_NAME = "auto_mpg_exam_dataset.csv"

# -----------------------------
# 1. CSV 읽기
# -----------------------------
df = pd.read_csv(FILE_NAME)

print("=== [1] 데이터 확인 ===")
print(df.head(), "\n")
print(df.describe(), "\n")

#%%
# -----------------------------
# 2. X, y 분리 (Pandas)
# -----------------------------
feature_cols = ["engine_size", "horsepower", "weight", "model_year"]
target_col = "mpg"

X_pd = df[feature_cols]        # (N, 4)
y_pd = df[[target_col]]        # (N, 1)  <- 2D 유지

# -----------------------------
# 3. MinMaxScaler 정규화
# -----------------------------
# X용 스케일러, y용 스케일러를 따로 사용
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

# fit_transform: 학습 + 변환
X_scaled_np = scaler_X.fit_transform(X_pd.values)    # (N, 4) -> 0~1
y_scaled_np = scaler_y.fit_transform(y_pd.values)    # (N, 1) -> 0~1

# PyTorch 텐서로 변환
X = torch.tensor(X_scaled_np, dtype=torch.float32, device=DEVICE)
y = torch.tensor(y_scaled_np, dtype=torch.float32, device=DEVICE)

print(f"X tensor shape: {X.shape}")  # (N, 4)
print(f"y tensor shape: {y.shape}")  # (N, 1)

#%%
# -----------------------------
# 4. Train / Test Split (PyTorch 방식)
# -----------------------------
N = X.shape[0]
test_ratio = 0.2
test_size = int(N * test_ratio)
train_size = N - test_size

indices = torch.randperm(N)
train_idx = indices[:train_size]
test_idx = indices[train_size:]

X_train = X[train_idx]
y_train = y[train_idx]
X_test = X[test_idx]
y_test = y[test_idx]

print(f"Train size: {train_size}, Test size: {test_size}\n")

#%%
# -----------------------------
# 5. 신경망(MLP) 모델 정의
# -----------------------------
class RegressionNet(nn.Module):
    def __init__(self, input_dim, hidden1=16, hidden2=8, output_dim=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Linear(hidden2, output_dim),
        )

    def forward(self, x):
        return self.net(x)

input_dim = len(feature_cols)  # 4
model = RegressionNet(input_dim).to(DEVICE)

print("=== [5] 모델 구조 ===")
print(model, "\n")

# -----------------------------
# 6. 손실 함수 & 옵티마이저
# -----------------------------
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

#%%
# -----------------------------
# 7. 학습 루프
# -----------------------------
num_epochs = 1000

loss_history = []

for epoch in range(1, num_epochs + 1):
    model.train()

    # Forward
    y_pred = model(X_train)
    loss = criterion(y_pred, y_train)

    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # ---- Loss 기록 ----
    loss_history.append(loss.item())

    if epoch % 100 == 0:
        print(f"[Epoch {epoch:4d}] Loss = {loss.item():.6f}")


print("\n=== 학습 완료 ===\n")


# -----------------------------
# 8. 학습 손실 곡선 시각화
# -----------------------------

plt.figure(figsize=(8, 5))
plt.plot(loss_history, label="Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss (MSE)")
plt.title("Training Loss Curve")
plt.grid(True)
plt.legend()
plt.show()


#%%
# -----------------------------
# 9. 테스트셋 평가 (RMSE, MAE, R^2)
# -----------------------------
model.eval() # 평가 모드 전환
with torch.no_grad(): #  추론시 불필요한 그래디언트 계산 비활성화
    y_test_pred_scaled = model(X_test)    # 스케일된 y (0~1 범위)

# 텐서를 numpy로 변환 (CPU로 가져오기)
y_test_scaled_np = y_test.cpu().numpy()              # (M, 1)
y_test_pred_scaled_np = y_test_pred_scaled.cpu().numpy()

# MinMaxScaler로 역정규화 → 원래 mpg 값으로 복원
y_test_true_orig = scaler_y.inverse_transform(y_test_scaled_np)         # (M, 1)
y_test_pred_orig = scaler_y.inverse_transform(y_test_pred_scaled_np)    # (M, 1)

# RMSE, MAE, R^2 계산 (numpy 사용)
mse = np.mean((y_test_pred_orig - y_test_true_orig) ** 2)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(y_test_pred_orig - y_test_true_orig))

y_mean = np.mean(y_test_true_orig)
ss_tot = np.sum((y_test_true_orig - y_mean) ** 2)
ss_res = np.sum((y_test_true_orig - y_test_pred_orig) ** 2)
r2 = 1 - (ss_res / ss_tot)

print("=== [평가 지표] ===")
print(f"RMSE: {rmse:.3f}")
print(f"MAE : {mae:.3f}")
print(f"R^2 : {r2:.3f}\n")

#%%
# -----------------------------
# 10. 임의 차량 1대 mpg 예측
#    예) engine_size=2.0, horsepower=150,
#        weight=1300, model_year=2020
# -----------------------------
test_car_dict = {
    "engine_size": 2.0,
    "horsepower": 150.0,
    "weight": 1300.0,
    "model_year": 2020.0,
}

test_car_df = pd.DataFrame([test_car_dict])   # (1, 4)

# X 스케일러로 정규화
test_car_scaled_np = scaler_X.transform(test_car_df.values)   # (1, 4)

test_car_scaled_tensor = torch.tensor(
    test_car_scaled_np, dtype=torch.float32, device=DEVICE
)

model.eval()
with torch.no_grad():
    pred_scaled = model(test_car_scaled_tensor)          # (1, 1) 스케일된 값
    pred_scaled_np = pred_scaled.cpu().numpy()
    pred_mpg_orig = scaler_y.inverse_transform(pred_scaled_np)[0, 0]

print("=== [특정 차량 mpg 예측] ===")
print("입력 값:", test_car_dict)
print(f"예측 연비(mpg): {pred_mpg_orig:.3f}")

# %% 실제 mpg와 예측 mpg를 나란히 표시하는 그래프
# CPU로 변환 & flatten
y_true = y_test_true_orig.flatten()
y_pred = y_test_pred_orig.flatten()

plt.figure(figsize=(10,5))
plt.plot(y_true, label="Actual MPG", marker='o')
plt.plot(y_pred, label="Predicted MPG", marker='x')
plt.title("Actual vs Predicted MPG (Test Set)")
plt.xlabel("Sample Index")
plt.ylabel("MPG")
plt.grid(True)
plt.legend()
plt.show()
# %%
