#%% ready
import numpy as np

#%% 통계
ary = np.array([1,2,3])
ary_batch = np.array([[1,2,3],[1,2,3],[1,2,3],[1,2,3]] )

print(ary.sum())
print(ary.mean()) 
print(ary.std()) # 표준편차
print(ary.var()) # 분산

print(ary_batch.sum())
print(ary_batch.sum())

# %% 사칙연산
print(ary * 10)
print(ary_batch * 10)
print(ary_batch / 10)
print(ary_batch + 10)
# %% dot
print(ary.dot([3,4,5]))
print(ary_batch.dot([3,4,5]))
# %%


