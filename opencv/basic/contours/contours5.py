import numpy as np
import cv2 as cv

#윤각선 정점갯수 줄이기 (근사값 찾기)

im = cv.imread('../../res/contour1.png')
if (type(im) is np.ndarray) == False : print('file read error');exit()

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

def onChange(x):
    pass

cv.namedWindow('Tracks')


cv.createTrackbar('thres', 'Tracks', 128, 255,onChange)
cv.createTrackbar('epsilon','Tracks',100,1000,onChange)

# cv.resizeWindow('Tracks',256,256)


def findExtreamPoint(_im,_approxPoly) : 
    
    #좌측 극점 
    _tmp = _approxPoly[ np.argsort(_approxPoly[:,0,1]) ]
    leftmost = tuple(_tmp[_tmp[:,:,0].argmin()][0])
    # leftmost = tuple(_approxPoly[_approxPoly[:,:,0].argmin()][0])

    #우측극점 
    _tmp = _approxPoly[ np.argsort(-_approxPoly[:,0,1]) ]
    rightmost = tuple(_tmp[_tmp[:,:,0].argmax()][0])
    # rightmost = tuple(_approxPoly[_approxPoly[:,:,0].argmax()][0])
        

    #상측극점 
    # print(_approxPoly[ np.argsort(-_approxPoly[:,0,1]) ])
    _tmp = _approxPoly[ np.argsort(-_approxPoly[:,0,0]) ]
    topmost = tuple(_tmp[_tmp[:,:,1].argmin()][0])


    #하측 극점 
    _tmp = _approxPoly[ np.argsort(_approxPoly[:,0,0]) ]
    bottommost = tuple(_tmp[_tmp[:,:,1].argmax()][0])

    # bottommost = tuple(_approxPoly[_approxPoly[:,:,1].argmax()][0])

    # print('leftmost',leftmost)
    # print('rightmost',rightmost)
    # print('topmost',topmost)
    # print('bottommost',bottommost)

    # print( np.argsort(_approxPoly[0],axis=0))

    cv.circle(_im,leftmost,16,(0,255,255),-1)
    cv.circle(_im,rightmost,16,(255,0,0),-1)
    cv.circle(_im,topmost,16,(0,0,255),-1)
    cv.circle(_im,bottommost,16,(0,255,0),-1)


while True:
    
    _key = cv.waitKey(20) & 0xff
    if _key == 27:
        cv.destroyAllWindows()
        break
    elif _key == ord('r'): print('epsilon , thres : ', _epsilon,_thres)

    _thres = cv.getTrackbarPos('thres', 'Tracks')
    _epsilon = cv.getTrackbarPos('epsilon','Tracks')
    

    ret, thresh = cv.threshold(imgray, _thres, 255, 0)
    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    _contours = [_contour  for _contour in contours if cv.contourArea(_contour) > 1000 ]

    # print(_contours)

    _im = im.copy()

    for _cnt in contours : 
        if cv.contourArea(_cnt) > 1000 : 
            _arcL = cv.arcLength(_cnt,True)
            _approxPoly = cv.approxPolyDP(_cnt, float(_epsilon)/1000 * _arcL,True)
            cv.drawContours(_im, [_approxPoly], 0, (0, 255, 0), 2)
            #끝점 구하기 
            findExtreamPoint(_im,_approxPoly)

    cv.imshow("result",_im)

