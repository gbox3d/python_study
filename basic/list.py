#%% container type unpacking

numbers = [1,2,3,4,5,6]

# _a, = numbers #erreor
*_a, = numbers
print(_a) # _a [1,2,3,4,5,6] 

*_a,b = numbers
print(_a) # _a -> [1,2,3,4,5] ,_b -> 6

# %%
print( [1,] + [2,])
print( (1,) + (2,))

# %%
