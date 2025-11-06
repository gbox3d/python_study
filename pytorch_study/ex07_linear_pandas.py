#%%
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd # CSV 파일을 읽기 위해 pandas를 import

# --- 1. 데이터셋 준비 ---

# 생성했던 CSV 파일 이름을 지정합니다.
FILE_NAME = 'dataset_100.csv' 
TRUE_W1, TRUE_W2, TRUE_B = 3.0, 5.0, 2.0 # 비교를 위한 실제 값

# Pandas를 사용해 CSV 파일 읽기
try:
    data = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"오류: '{FILE_NAME}' 파일을 찾을 수 없습니다.")
    print("먼저 generate_dataset.py 스크립트를 실행하여 데이터셋을 생성하세요.")
    exit()

# 데이터를 X (입력 특성)와 Y (타겟 값)로 분리
# X는 'x1', 'x2' 두 개의 컬럼을 가집니다.
X_pd = data[['x1', 'x2']]
# Y는 'y' 컬럼을 가집니다.
Y_pd = data[['y']]

# Pandas DataFrame을 PyTorch 텐서로 변환
# .values는 numpy 배열을 반환하며, torch.tensor로 감싸줍니다.
# 모델 학습을 위해 dtype=torch.float32로 설정하는 것이 중요합니다.
X_tensor = torch.tensor(X_pd.values, dtype=torch.float32)
Y_tensor = torch.tensor(Y_pd.values, dtype=torch.float32)

print(f"데이터 로드 완료. X shape: {X_tensor.shape}, Y shape: {Y_tensor.shape}")

#%%

# --- 1-2. Min-Max 정규화 (Normalization) ---
# 이 부분이 핵심입니다!

# X값들의 최소, 최대값 계산 (x1, x2 전체에서)
x_min = X_tensor.min() 
x_max = X_tensor.max()

# Y값들의 최소, 최대값 계산
y_min = Y_tensor.min()
y_max = Y_tensor.max()

# (value - min) / (max - min) 공식을 적용하여 0~1 사이 값으로 스케일링
X_scaled = (X_tensor - x_min) / (x_max - x_min)
Y_scaled = (Y_tensor - y_min) / (y_max - y_min)

print("데이터 정규화 완료.")

X_tensor = X_scaled
Y_tensor = Y_scaled


#%%

# --- 2. 모델 디자인 (입력 2, 출력 1) ---

# 입력 특성(feature)이 2개('x1', 'x2')
input_size = 2 
# 출력 값이 1개('y')
output_size = 1

model = nn.Linear(input_size, output_size)

# --- 3. Loss 및 Optimizer 정의 ---

learning_rate = 0.01 # 학습률
n_iters = 1000      # 학습 반복 횟수

loss_fn = nn.MSELoss() # 회귀 문제이므로 MSE (평균 제곱 오차) 사용
optimizer = optim.Adam(model.parameters(), lr=learning_rate) # Adam 옵티마이저 사용

#%%
print(f"모델 학습 시작 (Iterations: {n_iters}, LR: {learning_rate})...")

# --- 4. 학습 루프 ---

for epoch in range(n_iters):
    # 1. Forward pass: 모델 예측
    y_pred = model(X_tensor)
    
    # 2. Loss 계산
    loss = loss_fn(y_pred, Y_tensor)
    
    # 3. Backward pass: 그라디언트 계산
    loss.backward()
    
    # 4. Update weights: 가중치 업데이트
    optimizer.step()
    
    # 5. Zero gradients: 그라디언트 초기화
    optimizer.zero_grad()
    
    # 100번에 한 번씩 학습 과정 출력
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{n_iters}], Loss: {loss.item():.4f}')

print("...모델 학습 완료!")

#%%

# --- 5. 학습 결과 확인 ---
# 모델은 정규화된 데이터의 관계를 학습했으므로,
# 원본 가중치(3, 5, 2)와 직접 비교하는 것은 의미가 없습니다.
# 대신, 6번의 예측 결과를 통해 모델 성능을 확인합니다.
print("\n--- 학습 결과 ---")
print("모델이 정규화된 데이터에 대한 가중치를 학습했습니다.")
print("(w, b를 원본 값과 직접 비교하는 것은 의미 없음)")

# --- 6. 테스트 예측 (수정된 코드) ---
print("\n--- 테스트 예측 ---")
# x1=10, x2=10 일 때 예측
# 실제 값: (3 * 10) + (5 * 10) + 2 = 82
test_input_original = torch.tensor([[10.0, 10.0]], dtype=torch.float32)

# 1) 예측을 위해 테스트 입력도 "정규화"
#    (학습 때 사용한 x_min, x_max를 그대로 사용)
test_input_scaled = (test_input_original - x_min) / (x_max - x_min)

# 2) 모델로 예측 (결과도 0~1 사이의 정규화된 값으로 나옴)
predicted_scaled = model(test_input_scaled)

# 3) 결과를 다시 원래 스케일로 "역정규화"
#    (학습 때 사용한 y_min, y_max를 그대로 사용)
#    y = (y_scaled * (y_max - y_min)) + y_min
predicted_value = (predicted_scaled * (y_max - y_min)) + y_min

print(f"x1=10, x2=10 일 때 예측값: {predicted_value.item():.3f} (실제 값: 82.0)")
# %%
