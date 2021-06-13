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

# %%
