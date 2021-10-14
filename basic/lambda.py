#%%
_g = lambda x : x ** 2

print(_g(2))
# %%
__sum = lambda x,y : x+y
print(__sum(1,2))
# %%
def _inc(n) :
    return lambda x : x+n

_inc2 = _inc(2)

print(_inc2(5))
# %% map 
a = [1,2,3,4]
b = [5,6,7,8]

print( list (map(lambda x,y:x+y,a,b) ) )

#%% filter

c = [1,2,3,4,5,6,7,8,9]

print( list (filter(lambda x:x==2,c) )) # 참이면 남고 거짓이면 삭제 


# %%
