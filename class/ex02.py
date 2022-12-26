#%% 클래스 변수
class Ex02Class :
    className = "Ex02Class"
    def __init__(self, name, age) :
        self.name = name
        self.age = age
    
    def getClassName(self) :
        return self.className

#%%

a = Ex02Class("홍길동", 20)


print(a.className)
print(Ex02Class.className)

# %%
print(type(a))

# %%
if __name__ == "__main__":
    print("main")
