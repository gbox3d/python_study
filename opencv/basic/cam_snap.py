import cv2 as cv 
import sys
import time 
print(sys.argv)

#라즈베리는 -1 , 웹캠은 0
cap = cv.VideoCapture(-1)
#cap = cv.VideoCapture(0)

# python3 cam_snap.py 1920 1080
if len(sys.argv) == 3 :
    #해상도 세팅 
    #2592 × 1944 , 3280 × 2464 p
    #https://www.codingforentrepreneurs.com/blog/open-cv-python-change-video-resolution-or-scale
    print('set resolution {int(sys.argv[1])} , {int(sys.argv[2])}')
    cap.set(cv.CAP_PROP_FRAME_WIDTH,int(sys.argv[1]))
    cap.set(cv.CAP_PROP_FRAME_HEIGHT,int(sys.argv[2]))



# set_res(cap,1280,1024)

# cap.set(3, 1920)
# cap.set(4, 1080)

# time.sleep(1)

ret,frame = cap.read()

#해상도 얻기
print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))


cv.imwrite('test.png',frame)