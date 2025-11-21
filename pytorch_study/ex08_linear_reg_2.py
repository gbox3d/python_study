#%%
import torch
import torch.nn as nn
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#%%
# 0) Prepare data
# X_numpy 는 shape (100,1)
# y_numpy 는 shape  (100,)
X_numpy, y_numpy = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=4)
plt.plot(X_numpy, y_numpy, 'ro')
plt.show()

# 데이터 생성 후
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

# 0~1로 변환
X_scaled = scaler_x.fit_transform(X_numpy)
y_scaled = scaler_y.fit_transform(y_numpy.reshape(-1, 1))

# 텐서로 변환하여 학습 진행...
X = torch.from_numpy(X_scaled.astype(np.float32))
y = torch.from_numpy(y_scaled.astype(np.float32))


n_samples, n_features = X.shape

# 1) Model
# Linear model f = wx + b
input_size = n_features
output_size = 1
model = nn.Linear(input_size, output_size)

print(model.weight)
#%%
# 2) Loss and optimizer
learning_rate = 0.01

criterion = nn.MSELoss()
# optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)  
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
num_epochs = 600
#%%
# 3) Training loop

for epoch in range(num_epochs):
    # Forward pass and loss
    y_predicted = model(X)
    loss = criterion(y_predicted, y)
    
    # Backward pass and update
    loss.backward()
    optimizer.step()

    # zero grad before new step
    optimizer.zero_grad()

    if (epoch+1) % 100 == 0:
        print(f'epoch: {epoch+1}, loss = {loss.item():.4f}')

#%% Plotting the results
# 1. 정규화된 상태 그대로 예측값 뽑기
predicted_scaled = model(X).detach().numpy()

# 2. 텐서를 다시 넘파이로 (그리기 위해)
X_scaled_numpy = X.numpy()
y_scaled_numpy = y.numpy()

# 3. 그리기 (정렬 같은 복잡한 과정 없이 점으로 찍어서 확인)
plt.figure(figsize=(8, 6))

# 정답 데이터 (빨간 점)
plt.plot(X_scaled_numpy, y_scaled_numpy, 'ro', label='Real Data (0~1)')

# 예측한 데이터 (파란 점)
# 선으로 긋지 않고 점으로 찍으면('b.') 정렬(sort)할 필요도 없어 코드가 제일 짧습니다.
plt.plot(X_scaled_numpy, predicted_scaled, 'b.', label='Prediction (0~1)') 

plt.legend()
plt.title("Normalized Data & Prediction")
plt.show()
# %%
