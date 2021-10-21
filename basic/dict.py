#%%
_dict = {
    "a":1,
    "b":2,
    "c":3
}

for k,v in _dict.items() :
    print(k,v)
# %%
print( { k+'_TTA' : v for k,v in _dict.items() } )
# %%
