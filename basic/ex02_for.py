#%%
for i in range(0,10):
    print(i)
# %%
for i in range(0,10,2):
    print(i)
# %%
for i in range(10,0,-1):
    print(i)
# %%
for i,v in enumerate([9,8,7,6]):
    print( f'index:{i}, value:{v}')
# %%
_list = [i for i in range(2,16,2)]
print(f'{_list} , type {type(_list)}')
# %%
_items = ['png','jpeg','stop','gif']
for _item in _items:
    if _item == 'stop': 
        break

    print(_item)
# %%
