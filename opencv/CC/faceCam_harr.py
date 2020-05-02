import cv2 as cv
import sys 
import time

face_cascade = cv.CascadeClassifier('../data/haarcascades/haarcascade_frontalface_default.xml')
# face_cascade = cv.CascadeClassifier('../../data/haarcascades/haarcascade_upperbody.xml')

camDevice = 0;
if len(sys.argv) >=2 : camDevice = int(sys.argv[1])

print(camDevice)

cap = cv.VideoCapture(camDevice)

if cap.get(3) < 10 : 
    print('not found cam')
    exit()
else : 
    print(f'found cam : {cap.get(3),{cap.get(4)}}') 
    cap.set(3,640)
    cap.set(4,480)
    time.sleep(1)
    print(f'change resolution : {cap.get(3),{cap.get(4)}}') 


while(True) :
    # time.sleep(1)

    ret,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3, 5)

    _img = frame.copy()

    for (x,y,w,h ) in faces : 
        cv.rectangle(_img,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv.putText(_img,f'detect : {len(faces)} ',(10,50), cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv.LINE_AA)

    cv.imshow('frame',_img)

    _k = cv.waitKey(1) & 0xff
    if _k == 27 : break
    # if cv.waitKey(1) & 0xFF == ord('q') :
        # break

cap.release()
cv.destroyAllWindows()
