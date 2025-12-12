#%%
import numpy as np
import pandas as pd

print("np version:", np.__version__)
print("pd version:", pd.__version__)

#%%
np.random.seed(42)

N = 200

# 독립 변수 생성
engine_size = np.random.uniform(1.0, 5.0, N)        # 1.0 ~ 5.0 L
horsepower = np.random.uniform(70, 250, N)          # 70~250 hp
weight = np.random.uniform(900, 2000, N)            # 900~2000 kg
model_year = np.random.randint(2000, 2024, N)       # 2000~2023

print("독립 변수 생성 완료.")
#%%
# 실제 연비 계산식 (노이즈 포함)
noise = np.random.normal(0, 2.0, N)

mpg = (
    50
    - 3.2 * engine_size
    - 0.04 * horsepower
    - 0.005 * weight
    + 0.30 * (model_year - 2000)
    + noise
)

# 데이터프레임 구성
df = pd.DataFrame({
    "engine_size": engine_size,
    "horsepower": horsepower,
    "weight": weight,
    "model_year": model_year,
    "mpg": mpg
})

# 저장
df.to_csv("auto_mpg_exam_dataset.csv", index=False)
print("auto_mpg_exam_dataset.csv 생성 완료!")

# %%
