# %%
# module load

import numpy as np
import time

from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

# %%
image_path = '../res/1604097526765_image.jpg'
print('loading image')
src_image = Image.open(image_path)
# src_image
# display(src_image)
print(f'load complete , {src_image.size}')

# %%s

_tile_size = 5
_x = 0
_y = 0
_uw = src_image.size[0]/_tile_size
_uh = src_image.size[1]/_tile_size

for iy in range(0,_tile_size) :
    for ix in range(0,_tile_size) :
        _x = ix*_uw
        _y = iy*_uh
        print(f'{ix},{iy} / {_x},{_y}')
        _crop_img = ((src_image.crop([_x,_y,_x+_uw,_y+_uh])).resize((128,128),Image.ANTIALIAS))
        display(_crop_img)
        time.sleep(1)

# %%
