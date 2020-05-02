import cv2 as cv 
import numpy as np 
import sys

img = cv.imread('../../res/mina.png')
if (type(img) is np.ndarray) == False : 
    print('img file error')
    sys.exit()

_img = cv.resize(img,dsize=(72,128),interpolation=cv.INTER_AREA)

_img2 = cv.resize(img,dsize=(0,0),fx=0.5,fy=0.5,interpolation=cv.INTER_AREA)

cv.imshow('imgView',_img)
cv.imshow('imgView2',_img2)

cv.waitKey(0)

# while True : 
#     if cv.waitKey(20) & 0xff == 27 : break

cv.destroyAllWindows()