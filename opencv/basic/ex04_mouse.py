import numpy as np
import cv2 as cv

drag = False
mode = "circle"
ix,iy = -1,-1

def draw_function (event,x,y,flags,param) :
    global ix,iy,drag,mode
 
    if event == cv.EVENT_LBUTTONDOWN :
        # print('down')
        drag = True
        ix,iy=x,y
    
    elif event == cv.EVENT_MOUSEMOVE :
        if drag == True :
            if mode == "circle" :
                cv.circle(img,(x,y),5,(0,0,255),-1)
            else :
                cv.rectangle(img,(ix,iy),(x,y),(0,255,0)-1)

    elif event == cv.EVENT_LBUTTONUP :
        drag = False
        if mode == "rect":
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else :
            cv.circle(img,(x,y),5,(0,0,255),-1)


img = np.zeros( (512,512,3),np.uint8 )
cv.namedWindow('image')
cv.setMouseCallback('image',draw_function)
while(True) :
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    # print(k)
    if k == ord('m') :
        if mode == 'circle' : 
            mode = 'rect'
        else : 
            mode = 'circle'
    elif k == 27:
        break

cv.destroyAllWindows()


                
