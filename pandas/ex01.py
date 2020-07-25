#%%
#  https://dataitgirls2.github.io/10minutes2pandas/
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

#%%
s = pd.Series([1,3,5,np.nan,6,8])
type(s)
s

# %%

dates = pd.date_range('20130101', periods=6)
dates


# %%
df2 = pd.DataFrame({'A' : 1.,
                    'B' : pd.date_range('20200725', periods=4),
                    'C' : pd.Series((1,2,3,4),dtype='float32'),
                    'D' : np.array([3,5,7,9],dtype='int32'),
                    'E' : pd.Categorical(["test","train","test","train"]),
                    'F' : 'foo' },
                    index=['c001','c002','c003','c004']
                    )
df2

# %%
df2['A']

# %%
df2.B[1]


# %%
df2.tail(3)


# %%
df2.columns


# %%
df2.values

#%%
df2.values[1]
# %%
df2.values[1][3]

# %%

df2.loc[:,['A']]


# %%
# 행 단위로 데이터 얻기
df2.iloc[1]


# %%
df2.iloc[1]['B']


# %%
df2.loc['c001']

# %%
