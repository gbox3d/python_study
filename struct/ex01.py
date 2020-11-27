#%%
from struct import *

#%%
_ = pack('<L6s',1971,"hello".encode(),)

_data = unpack("<L6s",_)

print(_data)
# %%

_ = pack('<3s',b'jpg')

print(_)

_data = unpack('<3s',_)
print(_data)

# %%
