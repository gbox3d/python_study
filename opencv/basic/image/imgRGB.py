import cv2 as cv 
import numpy as np 
import sys

img = cv.imread('../res/mina.png')
if (type(img) is np.ndarray) == False : 
    print('img file error')
    sys.exit()

cv.imshow('imgView',img)

img_b,img_g,img_r = cv.split(img)

cv.imshow('RedChenel',img_r)
cv.imshow('BlueChenel',img_b)
cv.imshow('GreenChenel',img_g)

while True : 
    if cv.waitKey(20) & 0xff == 27 : break

cv.destroyAllWindows()