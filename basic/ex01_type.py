#%%
a = 10
a?
# %%
b = 10.0
b?
# %%
c = '10'
c?
#%%
d = 10 + 0j # complex number
d?

# %%
e = False
e?
# %%
print(type(a))
print(type(b))
print(type(c))
# %%
# 파인썬은 강한 타입 언어이다.
try :
    k = a + c
except Exception as e:
    print(e)

