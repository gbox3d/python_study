#%%
import numpy as np

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display

print('load module ok')

#%%
_img = Image.open('../res/shally.jpg')

display(_img)

print(_img.size)

# %%
import matplotlib
import matplotlib.pyplot as plt

np_img = np.array(_img)
print(np_img.shape)

plt.imshow(np_img)


# %%

# %%
