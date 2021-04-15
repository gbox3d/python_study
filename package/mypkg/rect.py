#%% http://pythonstudy.xyz/python/article/19-%ED%81%B4%EB%9E%98%EC%8A%A4
class Rect :
    count = 0 # static value
    def __init__(self,width,height) :
        self.width = width
        self.height = height
        Rect.count += 1
    def calcArea(self) :
        area = self.width * self.height
        return area
#%%
if __name__ == '__main__' :
    rect = Rect(3,4)
    print(rect.calcArea())
    print(rect.count)
# %%
