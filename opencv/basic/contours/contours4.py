import numpy as np
import cv2 as cv
im = cv.imread('../res/receipt.png')

if (type(im) is np.ndarray) == False:
    print('file read error')
    exit()

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# _contours = [_contour  for _contour in contours if cv.contourArea(_contour) > 10000 ]

# print( f"length : {len(_contours)}" )

# cv.drawContours(im,_contours,0,(0,255,0),2)

# cv.imshow('img',im)
# cv.imshow('thresh',thresh)


def onChange(x):
    pass


cv.namedWindow('Tracks')
# cv.namedWindow('image')

cv.createTrackbar('thres', 'Tracks', 0, 255, onChange)
cv.setTrackbarPos('thres','Tracks',205)

while True:
    _thres = cv.getTrackbarPos('thres', 'Tracks')
    # print(_thres)
    # ret, thresh = cv.threshold(imgray, _thres, 255, 0)
    # cv.imshow('imageThresh',thresh)

    _key = cv.waitKey(20) & 0xff
    if _key == 27:
        cv.destroyAllWindows()
        break
    elif _key == ord('r'):
        print('refresh : ', _thres)
        ret, thresh = cv.threshold(imgray, _thres, 255, 0)
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        _contours = [_contour  for _contour in contours if cv.contourArea(_contour) > 10000 ]
        
        _im = im.copy()
        cv.drawContours(_im, _contours, -1, (0, 255, 0), 2)

        _cnt = _contours[0]


# 끝점 구하기 
        leftmost = tuple(_cnt[_cnt[:,:,0].argmin()][0])
        rightmost = tuple(_cnt[_cnt[:,:,0].argmax()][0])
        topmost = tuple(_cnt[_cnt[:,:,1].argmin()][0])
        bottommost = tuple(_cnt[_cnt[:,:,1].argmax()][0])

        print(leftmost)
        print(rightmost)
        print(topmost)
        print(bottommost)

        cv.circle(_im,leftmost,16,(0,255,255),-1)
        cv.circle(_im,rightmost,16,(0,255,255),-1)
        cv.circle(_im,topmost,16,(0,255,255),-1)
        cv.circle(_im,bottommost,16,(0,255,255),-1)


        cv.imshow('imageThresh', thresh)
        cv.imshow('img', _im)
