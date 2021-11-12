#%%
import numpy as np
import cv2 as cv
from PIL import Image
from IPython.display import display


#%%
im = cv.imread('./contour1.png')
if (type(im) is np.ndarray) == False : print('file read error');exit()
display(Image.fromarray(im))
#%%
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
display(Image.fromarray(thresh))

#%%
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

optim_cnts = [cnt for cnt in contours if cv.contourArea(cnt) > 1000]

print(f'optim contours count: {len(optim_cnts)} ')
print(f'all contours count: {len(contours)} ')

_im = im.copy()
#그리기 
cv.drawContours(_im,
    optim_cnts, #윤각선 정보
    -1, #시작 인덱스 -1이면 모두그리기
    (0,255,0) #색
    ,3 #두께
)
display(Image.fromarray(_im))
#%%