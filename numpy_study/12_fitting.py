#%%
import numpy as np
import matplotlib.pyplot as plt

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

plt.scatter(x, y, label='data point')
plt.plot(x, m*x + c, 'r', label='fitted line')
plt.legend()
plt.show()

#%%
# x축 데이터 생성 (0부터 4π까지 200개의 점)
x = np.linspace(0, 4 * np.pi, 200)

# sin, cos 함수 계산
y_sin = np.sin(x)
y_cos = np.cos(x)

# sin 함수에 노이즈(잡음) 추가
# np.random.randn: 표준 정규 분포에서 샘플 추출
noise = 0.2 * np.random.randn(200)
y_sin_noisy = y_sin + noise

# 결과 시각화
plt.figure(figsize=(10, 6)) # 그래프 크기 조절
plt.plot(x, y_cos, 'g--', label='Cosine') # 초록색 점선
plt.plot(x, y_sin_noisy, 'o', markersize=3, label='Noisy Sine') # 작은 점으로 표시
plt.plot(x, y_sin, 'r-', linewidth=2, label='Pure Sine') # 빨간색 실선

# 그래프 제목 및 축 레이블 추가
plt.title('Sine and Cosine Waves with Noise')
plt.xlabel('x-axis (radians)')
plt.ylabel('y-axis (value)')
plt.legend()
plt.grid(True) # 그리드 추가
plt.show()

# %%
# 정규 분포를 따르는 데이터 생성
# 평균(mean) = 0, 표준편차(std_dev) = 1, 데이터 개수 = 1000
mu, sigma = 0, 1
data = np.random.normal(mu, sigma, 1000)

# 히스토그램 시각화
# bins: 막대의 개수, density: True로 설정하면 전체 면적이 1이 되도록 정규화
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data, bins=30, density=True, alpha=0.7, label='Histogram')

# 정규 분포 곡선 추가
# 확률 밀도 함수(PDF)를 계산하여 히스토그램 위에 겹쳐 그리기
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r', label='PDF')

plt.title('Histogram of Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.legend()
plt.show()
# %%

# 2D 그리드 생성
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
xx, yy = np.meshgrid(x, y)

# 2D 함수 계산 (예: 2D 가우시안 함수)
z = np.exp(-(xx**2 + yy**2) / 2)

# 2D 배열을 이미지로 시각화 (히트맵)
plt.figure(figsize=(8, 8))
# imshow: 2D 배열을 이미지로 표시
# cmap: 컬러맵 (viridis, gray, jet 등 다양하게 변경 가능)
plt.imshow(z, cmap='viridis', extent=[-5, 5, -5, 5])

plt.colorbar(label='Intensity') # 색상 막대 추가
plt.title('2D Gaussian Function Heatmap')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.show()
# %%
