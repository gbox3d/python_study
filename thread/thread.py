#%%
import threading
import time
 #%%
 
def _count(low, high):
    total = 0
    for i in range(low, high):
        total += 1
        time.sleep(1)
        print("Subthread", total)
    #서프 쓰레드 종료
    print("thread finish")


print('thread ready')

#%% start thread
t = threading.Thread(target=_count, args=(1, 10))
#주쓰레가 죽으면 같으죽는다. FALSE이면 주쓰레드와 관계없이 계속 동작한다.
t.daemon = False
t.start()

#%%
print("Main Thread wait")
time.sleep(5)
print("Main thread end")
#주쓰레드 종료 

# %%
