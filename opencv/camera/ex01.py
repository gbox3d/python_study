import cv2 as cv

cap = cv.VideoCapture(0)

#set camera 
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv.CAP_PROP_FPS, 60)

#get fps
print(f'fps : {cap.get(cv.CAP_PROP_FPS)}')

while(True) :
    ret,frame = cap.read()

    cv.imshow('frame',frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
cap.release()
cv.destroyAllWindows()