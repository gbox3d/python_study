# https://stackoverflow.com/questions/67219691/python-hash-function-that-returns-32-or-64-bits
#%%
import os
import hashlib
from datetime import datetime


#%%
print(int.from_bytes(hashlib.sha256(b"gbox3d").digest()[:4], 'little')) # 32-bit int
print(int.from_bytes(hashlib.sha256(b"gbox3d").digest()[:8], 'little')) # 64-bit int


# %%
value = str(datetime.now())
print(value)
print(int.from_bytes(hashlib.sha256(value.encode('utf-8')).digest()[:4], 'little'))

# %%
