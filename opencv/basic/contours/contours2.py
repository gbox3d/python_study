import numpy as np
import cv2 as cv

im = cv.imread('../../res/contour1.png')
if (type(im) is np.ndarray) == False : print('file read error');exit()

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# print( len(contours))

cnt = contours[0]
_mmt = cv.moments(cnt)
# print ("moment :" , _mmt)
cx = _mmt["m10"]/_mmt["m00"]
cy = _mmt["m01"]/_mmt["m00"]

print(f'cx : {cx},cy: {cy}')

print("area : " , cv.contourArea(cnt))
print("arcLength : " , cv.arcLength(cnt,True))

# cv.drawContours(im,[cnt],0,(0,255,255),3)

# for _contour in contours : print(cv.contourArea(_contour))

_contours = [_contour  for _contour in contours if cv.contourArea(_contour) > 1000 ]

print('윤각선 갯수 : ', len(_contours))

font = cv.FONT_HERSHEY_SIMPLEX

# print(_contours)

def contour_info (_cnt) : 
    _mmt = cv.moments(_cnt)
    
    x,y,w,h = cv.boundingRect(_cnt)
    aspect_ratio = w/h

    hull = cv.convexHull(_cnt)
    solidity = cv.contourArea(_cnt)/cv.contourArea(hull)
    equivalent_diameter = np.sqrt(4*cv.contourArea(_cnt)/np.pi) # 최적원 지름 구하기 

    minRect = cv.minAreaRect(_cnt) #  바운딩박스 값에 추가로 기울어진 각도까지 구한다.
    boxPts = cv.boxPoints(minRect)
    boxPts = np.int0(boxPts)
    cv.drawContours(im,[boxPts],0,(0,255,0),1)

#외각원 
    minCircle = cv.minEnclosingCircle(_cnt) 
    minCirclePos = np.int0(minCircle[0])
    minCircleR = int(minCircle[1])

    coronaSize = minCircleR - (equivalent_diameter/2)


    print(aspect_ratio,solidity,coronaSize)
    

    cx = int(_mmt["m10"]/_mmt["m00"])
    cy = int(_mmt["m01"]/_mmt["m00"])
    cv.drawContours(im,[_cnt],0,(0,0,255),3)
    cv.circle(im,(cx,cy),4,(255,0,0),-1)
    cv.rectangle(im,(x,y),(x+w,y+h),(0,255,0),thickness=1)
    
    cv.circle(im,(cx,cy),int(equivalent_diameter/2),(255,255,0),thickness=1)

    
    cv.circle(im,(minCirclePos[0],minCirclePos[1]),minCircleR,(255,255,255),thickness=1)
    
    cv.putText(im,f'{cx},{cy}',(cx,cy), font,0.25 ,(255,0,0),1,cv.LINE_AA)
    cv.putText(im,f'{solidity}',(cx,cy+10), font,0.25 ,(0,0,0),1,cv.LINE_4)
    cv.putText(im,f'{aspect_ratio}',(cx,cy+20), font,0.25 ,(0,0,0),1,cv.LINE_4)

#원인지 검사 
    if coronaSize < 5 and solidity > 0.8 and abs(1-aspect_ratio) < 0.1 : 
        cv.putText(im,"it is circle",(cx,cy-10),font,0.5,(0,0,255),1,cv.LINE_4)

# 끝점 구하기 
    leftmost = tuple(_cnt[_cnt[:,:,0].argmin()][0])
    rightmost = tuple(_cnt[_cnt[:,:,0].argmax()][0])
    topmost = tuple(_cnt[_cnt[:,:,1].argmin()][0])
    bottommost = tuple(_cnt[_cnt[:,:,1].argmax()][0])

    print(_cnt[_cnt[:,:,0].argmax()])

    print(leftmost,rightmost)

    cv.circle(im,leftmost,16,(0,255,0),-1)
    cv.circle(im,rightmost,16,(0,255,0),-1)
    cv.circle(im,topmost,16,(0,255,0),-1)
    cv.circle(im,bottommost,16,(0,255,0),-1)


contour_info( _contours[1])


cv.imshow("result",im)


while True : 
    if cv.waitKey(20) & 0xff == 27 : break

cv.destroyAllWindows()

# if cv.imwrite('../output/contours2.png',im) == True : print('save ok')
