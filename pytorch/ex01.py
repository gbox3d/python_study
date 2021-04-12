#%%
import cv2
import torch
import torchvision
import torch.backends.cudnn as cudnn

print(f' cv version : {cv2.__version__}')
print(f' torch version : {torch.__version__}')

#%%
_a = torch.Tensor([1,2,3])

print(_a[0])
print(_a[0].item())
# %%
