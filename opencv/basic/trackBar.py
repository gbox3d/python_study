import numpy as np 
import cv2 as cv 

print (cv.__version__)
def onChange(x) : 
    pass

img = np.zeros((512,512,3),np.uint8)
cv.namedWindow('Tracks')
cv.namedWindow('image')

cv.createTrackbar('R','Tracks',0,255,onChange)
cv.createTrackbar('G','Tracks',0,255,onChange)
cv.createTrackbar('B','Tracks',0,255,onChange)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'Tracks',0,1,onChange)

while True : 
    # cv.imshow('Tracks',img)
    cv.imshow('image',img)
    
    
    _k = cv.waitKey(20) & 0xff
    if _k == 27 : break
    _r = cv.getTrackbarPos('R','Tracks')
    _g = cv.getTrackbarPos('G','Tracks')
    _b = cv.getTrackbarPos('B','Tracks')
    s = cv.getTrackbarPos(switch,'Tracks')

    if s == 0 : 
        img[:] = 0
    else : 
        img[:] = [_b,_g,_r]




cv.destroyAllWindows()