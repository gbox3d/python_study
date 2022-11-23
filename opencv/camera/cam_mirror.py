import cv2 as cv

cap = cv.VideoCapture(0)
while(True) :
    ret,frame = cap.read()
    # _flip = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    _flip = cv.flip(frame,1)

    cv.imshow('frame',_flip)
    _k = cv.waitKey(1) & 0xff
    if _k == 27 : break
    # if cv.waitKey(1) & 0xFF == ord('q') :
        # break

cap.release()
cv.destroyAllWindows()