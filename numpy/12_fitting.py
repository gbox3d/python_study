#%%
import numpy as np
#%%
# 가상의 데이터 생성
x = np.linspace(0, 10, 50)
y = 2 * x + 1 + np.random.randn(50)

# 선형 회귀 계산
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
print("기울기 m =", m)
print("절편 c =", c)

# 결과 시각화
import matplotlib.pyplot as plt
plt.scatter(x, y, label='data point')
plt.plot(x, m*x + c, 'r', label='fitted line')
plt.legend()
plt.show()

# %%
