#%% region of images
# https://bkshin.tistory.com/entry/OpenCV-9-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%B0%EC%82%B0

import numpy as np
import cv2 as cv

from PIL import Image
from IPython.display import display


#%%
img = cv.imread('../../akb48.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
img[:,:,3] = 255
# print(img.shape)

display(Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)))

#%%
#마스크 비트멥 만들기 
# mask = np.zeros((367,550,3),np.uint8)
mask = np.zeros_like(img)
mask = cv.cvtColor(mask, cv.COLOR_BGR2BGRA)
mask[:,:,3] = 0

cv.rectangle(mask,
    (50,100),(150,200), #영역 
    (255,255,255,255), #color
    -1 # 칠하기
    )

display(Image.fromarray(mask))


#%%
masked = cv.bitwise_and(img, mask)
display(Image.fromarray(cv.cvtColor(masked, cv.COLOR_BGRA2RGBA)))
#%%
# masked_a = masked
#save result
cv.imwrite('../../../output/mask_nukki.png',masked)
# %%
