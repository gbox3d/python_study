#%%
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

#%%
df = pd.read_csv('data/100 Sales Records.csv')

#%%
#전체 열구하기 
print(df.columns)
# %%
# 시작점 기준 2줄보기
df.head(2)

# %%
# 첫번째 row 가져오기 0 부터시작 
print(df.iloc[0])
print(df.iloc[0]['Region'])
print(df.iloc[0][0])

# %%
print(df.iloc[:,0])
print(df.iloc[:,0][0])
#키값으로는 접근할수없다.  print(df.iloc[0]['Region'])
print(df.iloc[:,0][1])

# %%
#전체 행(x)갯수 구하기
len(df.iloc[:])

# %%
# 2차원 배열형식(numpy)으로 값얻어오기 [row,col]
df.values[0,5]

# %%
#value 는 numpy 배열형이다.
type(df.values)


# %%
