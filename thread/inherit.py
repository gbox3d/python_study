#%%
import threading
import random
import time

#%%
class MyThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)  
        self.result = 0
        self.index = args[0]
        self.a = kwargs['a']
        self.b = kwargs['b']
    
    def run(self):
        print(f"Subthread start {self.index}")
        self.result = random.randint(1, 3)
        time.sleep(self.result)
        print(f"Subthread end {self.index}")
        time.sleep(1)
        
#%%
for i in range(5):
    t = MyThread(args=(i,),kwargs={'a':1, 'b':2})
    t.start()

# %%
time.sleep(10)
print("Main thread end")