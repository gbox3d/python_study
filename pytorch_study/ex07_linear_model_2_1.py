# 1) Design model (input, output, forward pass with different layers)
# 2) Construct loss and optimizer
# 3) Training loop
#       - Forward = compute prediction and loss
#       - Backward = compute gradients
#       - Update weights
#%%
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

torch.set_printoptions(precision=4)

# here : f = 3 * x1 + 5 * x2 + 2

# 0) Training samples, watch the shape!
X = torch.tensor([
    [1, 1],  # x1=1, x2=1
    [2, 3],  # x1=2, x2=3
    [3, 2],  # x1=3, x2=2
    [4, 5]   # x1=4, x2=5
], dtype=torch.float32)

Y = torch.tensor([
    [10],
    [23],
    [21],
    [39]
], dtype=torch.float32)

n_samples, n_features = X.shape
print(f'#samples: {n_samples}, #features: {n_features}')

#%%
# --- 테스트 데이터 ---
# X_test = [[5, 6]]
X_test = torch.tensor([[5, 6]], dtype=torch.float32)

# Y_test = 3*5 + 5*6 + 2 = 47
Y_test = torch.tensor([[47]], dtype=torch.float32)

#%%
# 1) Design Model, the model has to implement the forward pass!
# Here we can use a built-in model from PyTorch
input_size = X.shape[1]
output_size = Y.shape[1]
print(f'Input size: {input_size}, Output size: {output_size}')
# we can call this model with samples X
model = nn.Linear(input_size, output_size) #숫자 input_size 개를 입력 받아서 숫자 output_size 개를 출력하는 선형모델을 만든다.

'''
class LinearRegression(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegression, self).__init__()
        # define diferent layers
        self.lin = nn.Linear(input_dim, output_dim)
    def forward(self, x):
        return self.lin(x)
model = LinearRegression(input_size, output_size)
'''

print(f'Prediction before training: f(5) = {model(X_test[0]).item():.3f}')

#%% 2) Define loss and optimizer
learning_rate = 0.01
n_iters = 1000

loss = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

loss_history = []

#%% 3) Training loop
for epoch in range(n_iters):
    
    # forward 함수 대신 model을 사용
    # predict = forward pass with our model
    y_predicted = model(X)

    # loss
    l = loss(Y, y_predicted)

    # calculate gradients = backward pass
    l.backward()

    # update weights
    optimizer.step()

    # zero the gradients after updating
    optimizer.zero_grad()

    if epoch % 10 == 0:
        [w, b] = model.parameters() # unpack parameters
        print(f'Epoch {epoch+1}: w = {w.squeeze().tolist()}, b = {b.item():.4f}, loss = {l.item():.4f}')
    loss_history.append(l.item())

print(f'Prediction after training: f(5) = {model(X_test[0]).item():.3f}')
#%%

# plot loss history
plt.plot(range(0, n_iters), loss_history)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss History')
plt.show()

# %% 

print(model(X_test))
print( loss(Y_test[0],model(X_test[0])) ) # 0 로스값 계산 
print( loss(Y_test[1],model(X_test[1])) ) # 1 로스값 계산 
print( loss(Y_test,model(X_test)) ) # 전체 로스값 계산 
# %%
