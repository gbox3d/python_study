# 입력 2개 출력 1개 예제 
#%%
import torch
import torch.nn as nn
import numpy as np
from torch.nn.modules.loss import MSELoss
import torch.nn.functional as F

from sklearn.preprocessing import StandardScaler # 데이터 정규화를 위한 라이브러리 

#%%
# _csv_data = np.loadtxt(fname='../data/gate.csv', delimiter=',',skiprows=1,dtype=np.float32)
_csv_data = np.loadtxt(fname='../data/wine.csv', delimiter=',',skiprows=1,dtype=np.float32)

__X = _csv_data[:,1:]

#데이터 정규화
scaler = StandardScaler()
# 메소드체이닝(chaining)을 사용하여 fit과 transform을 연달아 호출합니다
X = torch.tensor(scaler.fit(__X).transform(__X),dtype=torch.float32) # 정규화시킨 값으로 텐서 생성

Y = torch.tensor(_csv_data[:,[0]],dtype=torch.float32)

print(X.size())
print(Y.size())
# %%
class NeurelNet(nn.Module) :
    def __init__(self):
        super(NeurelNet,self).__init__()
        self.l1 = nn.Linear(13,64)
        self.l2 = nn.Linear(64,1)

    def forward(self,x) :
        out = F.relu(self.l1(x))
        out = F.relu(self.l2(out))
        return out
model = NeurelNet()

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

    if epoch%1000 == 0 :
        print(f'loss = {l.item()}')

# %%
print(model( X[0]) , Y[0] )
print(model( X[150]) , Y[150] )
# %%
