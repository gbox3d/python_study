# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# list 선언하기

# %% typle
_tuple = (1,2,3,4,5)
print(_tuple)


# %% tuple 은 수정 불가능하다.
# _list[1] = 0
print(_tuple[1])


# %%
for v in _tuple :
    print(v)

# %%

_list = [ v for v in _tuple]
print(_list)
# %%
# 리스트 덧씌우기
__list = [_list]
print(__list)
# %%
__list[0][2] = 20
print(__list)
# %%
