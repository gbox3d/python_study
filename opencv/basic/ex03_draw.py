import numpy as np
import cv2 as cv

#비트멥 만들기 
img = np.zeros((512,512,3),np.uint8)

cv.line(img,(0,0),(500,500),
(255,0,0) # BRG color
,5)

cv.rectangle(img,
(384,0),(510,128), #영역 
(0,255,0), #color
3)

cv.circle(img,
(447,63),  #중심정 
63, #지름  
(0,0,255), 
-1 # 칠하기 
)

cv.ellipse(img,(256,256),(100,50),0,0,180,(0,255,255),-1)

#폴리건 그리기 
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
print(pts)
pts = pts.reshape((-1,1,2))
print(pts)
cv.polylines(img,[pts],True,(0,255,255))

#텍스트 출력 
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV ',(10,500), font, 0.5,(255,255,255),2,cv.LINE_AA)

cv.imwrite('../output/test.png',img)

print("save ok..")
