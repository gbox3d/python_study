# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from PIL import Image
from PIL import ImageDraw
import os
import argparse

import numpy as np
from IPython.display import display

print(f'PIL version {Image.__version__}')


# %%
_img = Image.open('../res/shally.jpg')

print(_img.size)
print(_img.size[0])
# _img
display(_img)


# %%
# print(800*_img.size[0])
_ratio = 800/_img.size[0]

print(_ratio)

_size = (int(_img.size[0] * _ratio),int(_img.size[1] * _ratio))

print(_size)
_img_resized = _img.resize( _size,Image.ANTIALIAS)

display(_img_resized)


# %%
_imgout = Image.new(mode='RGB',size=(800,600),color=(255,0,0))

_imgout.paste(_img_resized)

display(_imgout)

