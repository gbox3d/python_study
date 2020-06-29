# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display

import time
import cv2 as cv

print( f'cv version : {cv.__version__}')


# %% opencv -> pil , array -> list
_img_np = cv.imread('../res/Lenna.png')

#포멧 변환 
_img_np = cv.cvtColor(_img_np,cv.COLOR_BGR2RGB)
display( Image.fromarray( _img_np))


# %% 카메라 입력
cap = cv.VideoCapture(0)
print( f'frame width{cap.get(cv.CAP_PROP_FRAME_WIDTH)} , height : ${cap.get(cv.CAP_PROP_FRAME_HEIGHT)}' )
time.sleep(1)
ret,frame = cap.read()
frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
display( Image.fromarray(frame))
time.sleep(1)
cap.release()
print('capture ok')

#%%
_img = Image.open('../res/Lenna.png')
type(_img)

img =  np.array(_img)
img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
type(img)
cv.imshow('image',img)
# cv.waitKey(0)

k = cv.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv.imwrite('messigray.png',img)
    cv.destroyAllWindows()

cv.destroyAllWindows()



# %%
