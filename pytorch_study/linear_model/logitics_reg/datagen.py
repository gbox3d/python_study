#%%
import numpy as np
import pandas as pd

np.random.seed(42)

N = 2000  # 샘플 수 (시험용 적당)

# Feature 생성
study_time = np.random.normal(3, 1.5, N).clip(0, 8)    # 하루 공부시간 (0~8시간)
attendance = np.random.normal(85, 10, N).clip(50, 100) # 출석률 (50~100%)
sleep_hours = np.random.normal(6.5, 1.2, N).clip(3, 10) # 수면시간 (3~10시간)
stress_level = np.random.normal(5, 2, N).clip(1, 10)    # 스트레스 (1~10)

# 실제적인 합격 확률(Logistic 형태)
# 공부시간 많을수록 +, 출석 좋으면 +, 스트레스 높으면 -
logit = (
    0.8 * study_time +
    0.05 * attendance -
    0.4 * stress_level -
    2
)

# Sigmoid 변환 → 확률
prob_pass = 1 / (1 + np.exp(-logit))

# 0/1 타겟 생성
pass_label = (prob_pass >= 0.5).astype(int)

# 데이터프레임 구성
df = pd.DataFrame({
    "study_time": study_time,
    "attendance": attendance,
    "sleep_hours": sleep_hours,
    "stress_level": stress_level,
    "pass": pass_label
})

df.to_csv("pass_dataset.csv", index=False)
print("pass_dataset.csv 생성 완료!")

# %%
