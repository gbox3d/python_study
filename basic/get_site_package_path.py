#%%
import sysconfig
print(sysconfig.get_paths()["purelib"])
# %%
import site
print(site.getsitepackages())

# %%
