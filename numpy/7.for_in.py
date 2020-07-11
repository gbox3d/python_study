# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### forin 을 활용한 필터링(골라내기) 
# 
# 문법  
# (출력값) for 값  in numpy배열 (최종 출력 여부를 판단하는 조건)

# %%
import numpy as np

_test_np = np.array([1,2,3,4,5,6])

#print( [_test_np  for _contour in contours if cv.contourArea(_contour) > 1000 ]

# %% [markdown]
# 
# 전체 데티어 덤프하기  
# 

# %%
print( [value  for value in _test_np ])

# %%
# 나머지가 0이 아닌 값만 골라내기
print( [_v for _v in _test_np if _v %2])


# %%
### zip 응용
_a = np.array([1,2,3,1])
_b = np.array([6,7,8,9])

#모두 출력
print( [ _v for _v in zip(_a,_b)  ])


#인덱스가 2 인것만 출력
_zip = [ _v for _v in zip(_a,_b) if _v[0] == 2 ]
print( _zip )



# %%
