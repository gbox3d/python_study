#https://mingrammer.com/introduce-comprehension-of-python/

#%%
eleven_numbers = [i for i in range(11)]
print(eleven_numbers)

#%%
print( [i%2 for i in eleven_numbers] )
print( [i for i in eleven_numbers if i % 2 == 0] )


# %%
epithets = ['sweet', 'annoying', 'cool', 'grey-eyed']
names = ['john', 'alice', 'james']
epithet_names = [(e, n) for e in epithets for n in names]
print(epithet_names)
# %%
