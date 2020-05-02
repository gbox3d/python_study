import cv2 as cv 
import numpy as np 
import sys

img = cv.imread('../res/mina.png')
if (type(img) is np.ndarray) == False : 
    print('img file error')
    sys.exit()

cv.imshow('imgView',img)

while True : 
    if cv.waitKey(20) & 0xff == 27 : break

cv.destroyAllWindows()