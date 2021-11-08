#%%
import torch
import torch.nn as nn
import numpy as np

#%%
_csv_data = np.loadtxt(fname='../data/regress.csv',delimiter=',',skiprows=0,dtype=np.float32) 
print(_csv_data)
# %%
X = torch.tensor(_csv_data[:,[0]],dtype=torch.float32)
Y = torch.tensor(_csv_data[:,[1]],dtype=torch.float32)

print(X)
print(Y)

# %%
class NeurelNet(nn.Module) :
    def __init__(self,in_size,out_size):
        super(NeurelNet,self).__init__()
        self.l1 = nn.Linear(in_size,out_size)
    def forward(self,x) :
        out = self.l1(x)
        return out
model = NeurelNet(in_size=1,out_size=1)

for param in model.parameters() :
    print(param)
# %%
loss = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.01)
print('loss function ready')
#%%
for epoch in range(1000) :
    _Y = model(X)
    l = loss(Y,_Y)

    l.backward()
    optimizer.step()
    optimizer.zero_grad()

    if epoch%100 == 0 :
        print(f'loss = {l.item()}')
#%%
print(model(torch.tensor([15],dtype=torch.float32))) # 15*3+5 = 50
# %%
