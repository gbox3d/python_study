#%%
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np


#%%
#data frame 만들기 
df = pd.DataFrame((np.random.rand(10,4) * 100).astype(np.int),
    index=[ f'st_num{i}' for i in range(10) ],
    columns=['kor','mat','eng','prg']

)

print(df)

# %%
df.to_csv('test.csv')

# %%
