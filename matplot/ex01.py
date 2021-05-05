#%%
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


print(matplotlib.__version__)

# %%
plt.xlabel('city')
plt.ylabel('zombie')
plt.title('zombie status')
plt.plot(["seoul","tokeyo","sangah"],[12,200,150])
plt.show()


#%%
a = [x for x in range(-5,5)]
b = [y for y in range(0,10)]

print(a)
print(b)

plt.plot(a,b)

plt.show()

# %%
img=mpimg.imread('../res/image2.jpg')
imgplot = plt.imshow(img)

# %%
plt.plot([1,2,3],[100,50,70])
plt.show()


# %%
