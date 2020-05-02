import numpy as np
import cv2 as cv

def isCircle (_cnt) :
    x,y,w,h = cv.boundingRect(_cnt)
    aspect_ratio = w/h
    squareRate = abs(1-aspect_ratio) #정사각형 근접비율 0이면 완벽한 정사각형

    hull = cv.convexHull(_cnt)
    solidity = cv.contourArea(_cnt)/cv.contourArea(hull)
    equivalent_diameter = np.sqrt(4*cv.contourArea(_cnt)/np.pi) # 최적원 지름 구하기 
    Null,minCircleR = cv.minEnclosingCircle(_cnt) 
    coronaSize = minCircleR - (equivalent_diameter/2)

    # index, parent , area

    if coronaSize < 5 and solidity > 0.8 and squareRate < 0.1 : 
        return True
    else :
        return False



im = cv.imread('../res/tg3.JPG')

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


# for index ,hr in  enumerate(hierarchy[0]) : 
    # if hr[0] != -1 && cv.contourArea() :  
    # if cv.contourArea(contours[index]) > 1000 : print(hr, cv.contourArea(contours[index]))

# print(hierarchy)


_contours = [ (idx,hr,contours[idx],cv.contourArea( contours[idx] ))  for idx,hr in enumerate(hierarchy[0]) if cv.contourArea( contours[idx] ) > 1000 ]

for _contour in _contours : 
    
    _cnt = _contour[2]
    
    x,y,w,h = cv.boundingRect(_cnt)
    aspect_ratio = w/h
    squareRate = abs(1-aspect_ratio) #정사각형 근접비율 0이면 완벽한 정사각형

    hull = cv.convexHull(_cnt)
    solidity = cv.contourArea(_cnt)/cv.contourArea(hull)
    equivalent_diameter = np.sqrt(4*cv.contourArea(_cnt)/np.pi) # 최적원 지름 구하기 
    Null,minCircleR = cv.minEnclosingCircle(_cnt) 
    coronaSize = minCircleR - (equivalent_diameter/2)

    # index, parent , area
    print( _contour[0],_contour[1][3],cv.contourArea(_cnt),coronaSize ,isCircle(_cnt))

    # if coronaSize < 5 and solidity > 0.8 and squareRate < 0.1 : 
        
    # else :
    #     print( _contour[0],_contour[1][0],coronaSize ,"not circle")


    





    
    

# print(_contours)

# font = cv.FONT_HERSHEY_SIMPLEX
# for _cnt in contours : 
#     cv.drawContours(im,[_cnt],0,(0,0,255),3)
#     _mmt = cv.moments(_cnt)
#     cx = int(_mmt["m10"]/_mmt["m00"])
#     cy = int(_mmt["m01"]/_mmt["m00"])
#     cv.circle(im,(cx,cy),8,(255,0,0),-1)
#     cv.putText(im,f'{cx},{cy}',(cx,cy), font,0.5 ,(0,255,0),2,cv.LINE_AA)

# cv.imshow('temp',im)
# cv.waitKey(0)
# cv.destroyAllWindows()
#
# if cv.imwrite('../output/app_1.png',im) == True : print('save ok')
