import cv2 as cv

cap = cv.VideoCapture(0)
while(True) :
    ret,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    cv.imshow('frame',gray)
    _k = cv.waitKey(1) & 0xff
    if _k == 27 : break
    # if cv.waitKey(1) & 0xFF == ord('q') :
        # break

cap.release()
cv.destroyAllWindows()