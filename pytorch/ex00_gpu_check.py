#%%
import torch
print(torch.__version__)
print(f'cuda is available {torch.cuda.is_available()}')
#%%
# torch.rand(3).to('cuda')
count = torch.cuda.device_count()
for i in range(0,count):
    print(f'gpu {i} : {torch.cuda.get_device_name(i)}'  )
print( f'gpu count : {torch.cuda.device_count()}')

# %% 에러가 안나면 쿠다가 잘 잡힌것
a = torch.rand(3).to('cuda')
print(a)
# 출력 결과 : tensor([0.2463, 0.6583, 0.1663], device='cuda:0')
# %%
