# https://skillmemory.tistory.com/entry/tqdm-%EC%82%AC%EC%9A%A9%EB%B2%95-python-%EC%A7%84%ED%96%89%EB%A5%A0-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%B0%94
#%% 
import time
from tqdm import tqdm

#%%
for i in tqdm(range(100)):
    time.sleep(0.1)
print("Done")
    
# %%
