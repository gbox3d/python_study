import numpy as np 
import cv2 as cv

def onChange(x) : 
    pass

face_cascade = cv.CascadeClassifier('../data/haarcascades/haarcascade_frontalface_default.xml')
# face_cascade = cv.CascadeClassifier('../../data/haarcascades/haarcascade_upperbody.xml')

img = cv.imread('../res/mina.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.namedWindow('tracks')
cv.createTrackbar('scale','tracks',5,10,onChange)
cv.createTrackbar('minNeigh','tracks',13,100,onChange)


while True: 

    _scale = cv.getTrackbarPos('scale','tracks')
    _minNeigh = cv.getTrackbarPos('minNeigh','tracks')

    print(_scale,float(_minNeigh)/10)

    faces = face_cascade.detectMultiScale(gray,float(_minNeigh)/10, _scale)
    
    _img = img.copy()
    for (x,y,w,h ) in faces : 
        cv.rectangle(_img,(x,y),(x+w,y+h),(0,255,0),2)

    cv.imshow('img',_img)

    # cv.waitKey(0)
    _k = cv.waitKey(1) & 0xff
    if _k == 27 : break


cv.destroyAllWindows()
