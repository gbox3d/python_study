# 입력 2개 출력 1개 예제 
#%%
import torch
import torch.nn as nn
import numpy as np
from torch.nn.modules.loss import MSELoss
import torch.nn.functional as F

#%%
_csv_data = np.loadtxt(fname='../data/gate.csv', delimiter=',',skiprows=1,dtype=np.float32)
# _csv_data = np.loadtxt(fname='../data/wine.csv', delimiter=',',skiprows=1,dtype=np.float32)

X = torch.tensor(_csv_data[:,0:2],dtype=torch.float32) 
Y = torch.tensor(_csv_data[:,[2]],dtype=torch.float32)

print(X.size())
print(Y.size())
# %%
class NeurelNet(nn.Module) :
    def __init__(self,in_size,hidden_size,out_size,):
        super(NeurelNet,self).__init__()
        self.l1 = nn.Linear(in_size,hidden_size)
        self.l2 = nn.Linear(hidden_size,out_size)
        # self.l3 = nn.Linear(128,out_size)
        

    def forward(self,x) :
        out = F.relu(self.l1(x))
        out = self.l2(out)
        # out = F.relu(self.l3(out))
        return out
model = NeurelNet(in_size=2,hidden_size=10,out_size=1)

for param in model.parameters() :
    print(param)

# %%
loss = nn.MSELoss()
optimizer = torch.optim.SGD(params=model.parameters(),lr=0.01)

#%%
for epoch in range(10000) :
    _Y = model(X)
    l = loss(Y,_Y)
    l.backward()

    optimizer.step()
    optimizer.zero_grad()

    if epoch%100 == 0 :
        print(f'loss = {l.item()}')

# %%