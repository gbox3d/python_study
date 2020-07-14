#%%
import threading
import time
 
def _count(low, high):
    total = 0
    for i in range(low, high):
        total += 1
        time.sleep(1)
        print("Subthread", total)
    print("thread finish")

print('thread ready')

 
#%%
t = threading.Thread(target=_count, args=(1, 10))
#주쓰레가 죽으면 같으죽는다. FALSE이면 주쓰레드와 관계없이 계속 동작한다.
t.daemon = True
t.start()

print("Main Thread wait")
time.sleep(3)
print("Main thread end")

# %%
