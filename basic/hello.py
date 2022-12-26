#%%
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, %s!" % self.name)
        
if __name__ == "__main__":
    _HelloWorld = HelloWorld("World")
    _HelloWorld.say_hello()
# %%
