# 1) Design model (input, output, forward pass with different layers)
# 2) Construct loss and optimizer
# 3) Training loop
#       - Forward = compute prediction and loss
#       - Backward = compute gradients
#       - Update weights
# 활성함수와 은닉층을 이용하여 xor 문재 해결하기
# %%
import torch
import torch.nn as nn

torch.set_printoptions(precision=4)

X = torch.tensor([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=torch.float32)
Y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

# Fully connected neural network with one hidden layer
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        # no activation and no softmax at the end
        return out
model = NeuralNet(
    2, # 입력 갑은 두개 
    10, # 히드레이어의 크기
    1 # 최종 출력크기 
    )
# %% 
# 2) Define loss and optimizer
learning_rate = 0.01
n_iters = 1000

loss = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# %% 3) Training loop
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

    # a = type(model.parameters())
    # print(a)
    # print(l)

    if epoch % 100 == 0:
        print(l.item())
    #     [w, b] = model.parameters()  # unpack parameters
    #     print('epoch ', epoch+1, ': w = ', w[0][0].item(), ' loss = ', l)

# print(f'Prediction after training: f(5) = {model(X_test[0]).item():.3f}')
#%%
for param in model.parameters():
    # print(type(param), param.size())
    print(param)

# %%
pred = model(torch.tensor([1,0],dtype=torch.float32))
print(pred)

pred = model(torch.tensor([0,0],dtype=torch.float32))
print(pred)
# %%
