#%% 텐서 기초 
# import cv2
import torch
import numpy as np

# print(f' cv version : {cv2.__version__}')
print(f' torch version : {torch.__version__}')

#%%
_a = torch.Tensor([1,2,3])

print(_a[0])
print(_a[0].item())
# %%
# 빈 텐서 만들기 
x = torch.empty(3) # 갯수를 넣어줌 
print(x)
y = torch.empty(3,2)
print(y)
# %%
x = torch.rand(3)
print(x)
# %%
x = torch.ones(3,2)
print(x)
print(x.dtype)
print(x.size())
x = torch.ones(3,2,dtype=torch.int64)
print(x)

# %%
x = torch.Tensor([1,2])
y = torch.Tensor([3,4])

print(x+y)
print(x-y)
print(x/y)

z = torch.add(x,y)
print(z)

# %%
x = torch.rand(5,3)
print(x)
print( x[1,:] ) # 1 행 모두 출력
print( x[ : , 2]) # 2행 모두 출력
# %%
x = torch.rand(4,4)
print(x)
print(x.view(16))
print(x.view(-1,8))

# %% numpy 변환 , torch-> numpy
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)

a.add_(1)
print(b) # 동일한 메모리 공간에 데이터를 저장함 
# %% numpy -> torch
a = np.ones(5)
print(a)
b = torch.from_numpy(a)
print(b)
# %% torch(cuda) -> numpy
if torch.cuda.is_available() : 
    print('cuda on')
    device = torch.device("cuda")
    x = torch.ones(5,device=device) # 처음부터 cuda로 생성 
    y = torch.ones(5)
    y = y.to(device) # cpu -> cuda
    z = x * y
    print(z)
    print(z.to('cpu'))
    print(z.to('cpu').numpy()) # cuda -> cpu -> numpy
else :
    print('no cuda')
# %%
# max 
x = torch.rand(3,5)
print(x)

print( torch.max(x) ) # 전체중 가장큰값

print( torch.max(x,1) ) # 한줄 한줄 에서 가각 가장 큰값 구하기(인덱스토 구해짐)


# %%
