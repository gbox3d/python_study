import numpy as np 
import cv2 as cv 

x = np.uint8([1,2,3])
y = np.uint8([5,4,3])

print ( cv.add(x,y) )

#(y,x,pixelnum)
_zeroImg = np.zeros((256,128,3),np.uint8)

_zeroImg[10:50,10:30] = [0,0,255]

cv.imshow('imgage',_zeroImg)

print ('esc to exit')

while True :
    if cv.waitKey(20) & 0xff == 27 : break

cv.destroyAllWindows()