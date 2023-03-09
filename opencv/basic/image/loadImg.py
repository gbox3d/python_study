#%%
import cv2 as cv 
import numpy as np 
import sys

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display
#%% 고수준 로더 사용 
img = cv.imread('../../akb48.jpg')

display(Image.fromarray(cv.cvtColor(img,cv.COLOR_BGR2RGB)))

#%% 디코더 사용 
with open('../../akb48.jpg',"rb") as fd:
    _data = fd.read()
    img_np = cv.imdecode(np.fromstring(_data, np.uint8), cv.IMREAD_COLOR)
    cv.cvtColor(img_np, cv.COLOR_BGR2RGB, img_np)
    display(Image.fromarray(img_np))

    
# %%
