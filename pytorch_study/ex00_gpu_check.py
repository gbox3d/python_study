#%%
import torch
print(torch.__version__)
print(f'cuda is available {torch.cuda.is_available()}')

#%%
# torch.rand(3).to('cuda')
print(f"cuda version : {torch.version.cuda}") # 10.2 이상
count = torch.cuda.device_count()
print( f'gpu count : {torch.cuda.device_count()}')

for i in range(count):
    name = torch.cuda.get_device_name(i)
    mem_gb = torch.cuda.get_device_properties(i).total_memory / 1024**3
    print(f"gpu {i} : {name} memory: {mem_gb:.2f} GB")

# %% 에러가 안나면 쿠다가 잘 잡힌것
a = torch.rand(3).to('cuda')
print(a)
# 출력 결과 : tensor([0.2463, 0.6583, 0.1663], device='cuda:0')
# %%
print (f"PyTorch version:{torch.__version__}") # 1.12.1 이상
print(f"MPS 장치를 지원하도록 build 되었는지: {torch.backends.mps.is_built()}") # True 여야 합니다.
print(f"MPS 장치가 사용 가능한지: {torch.backends.mps.is_available()}") # True 여야 합니다.

#%%
print(f"GPU 장치를 지원하도록 build 되었는지: {torch.backends.cuda.is_built()}") # True 여야 합니다.

