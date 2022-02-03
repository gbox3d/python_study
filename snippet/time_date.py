#%%
import sys
# import pytz
from pytz import timezone, utc,all_timezones
from datetime import datetime
import time

print(sys.version)
#%%
now = datetime.now()
print("now =", now)
# %%



# %%
for tz in all_timezones:
    print(tz)
# %%
KST = timezone('Asia/Seoul')
print(KST.localize(now))
# %%
TW = timezone('Asia/Taipei')
now = datetime.now()
now.replace(tzinfo=TW)
print(now)

# %%
now = datetime.utcnow()
print(now)
KST = timezone('Asia/Seoul')
print(KST.localize(now))
print(now.astimezone(KST))
# %%
