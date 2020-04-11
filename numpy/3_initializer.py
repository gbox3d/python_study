import numpy as np
# import matplotlib.pyplot as plt

arr2 = np.zeros(10)
print(arr2)
arr3 = np.zeros(10,dtype=np.uint8)
print(arr3)

print(np.ones(10))

print(np.ones((3,2),dtype=np.int))

#0~10까지 1씩 증가하는 배열 만들기
print(np.arange(0,10,1))


# 2x3 의 2차원 배열 만들기
print(np.arange(6).reshape(2,3))

# def f(t):
#     return np.exp(-t) * np.cos(2*np.pi*t)

# #0~5 까지 0.01 단위로 쪼개서 배열만들기 
# t1 = np.arange(0.0, 5.0, 0.01)

# print(t1)

# # plt.plot(t1, f(t1))

# # plt.show()
