import cv2 as cv
import numpy as np
events = [i for i in dir(cv) if 'EVENT' in i]
print( events )

mode = 1
def _mouseEvent(event,x,y,flags,param) : 
    print(event)
    if event == cv.EVENT_LBUTTONDOWN : 
        if mode : 
            cv.circle(img,(x,y),32,(0,0,255),-1)
        else : 
            cv.rectangle(img,(x-16,y-16),(x+16,y+16),(0,255,255),-1)

img = np.zeros((512,512,3),np.uint8)
cv.namedWindow('img1')
cv.setMouseCallback('img1',_mouseEvent)

while True : 
    cv.imshow('img1',img)
    _k = cv.waitKey(20) & 0xff
    
    if _k  != 0xff : 
        print(ord('m'),_k)
        if _k  == ord('m') : mode = not mode
        elif _k  == 27 : break # esc to exit

cv.destroyAllWindows()


