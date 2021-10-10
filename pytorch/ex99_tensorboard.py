#%%
import torch
from torch.utils.tensorboard import SummaryWriter

#%%
hist = SummaryWriter()

for x in range(314) :
    y = torch.sin(torch.tensor(x/100))
    hist.add_scalar('sinpluse',y,x)
    print(x,y)
print('done')

# %%
