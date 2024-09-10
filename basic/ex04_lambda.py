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

#%% 3 보다 작으면 0 크면 1
_list = [5,8,2,6,1,9,3,7,4]

map_list = list(map(lambda x:0 if x<3 else 1,_list))

print(map_list)


#%% filter

c = [1,2,3,4,5,6,7,8,9]

print( list (filter(lambda x:x==2,c) )) # 참이면 남고 거짓이면 삭제 


# %% 
_list = [i for i in range(1,11)]
print( list(filter(lambda x:x%2==0,_list)) )

#%% reduce
from functools import reduce

_list = [i for i in range(1,11)]
print(_list)
print(reduce(lambda x,y:x+y,_list))

# %%  

