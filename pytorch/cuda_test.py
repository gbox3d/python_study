#%% 에러 안나면 cuda 성공
import torch
a = torch.rand(3).to('cuda')
# %%
print(a)
# %%
