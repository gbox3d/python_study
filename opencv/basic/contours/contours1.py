import numpy as np
import cv2 as cv

im = cv.imread('../../res/contour1.png')
if (type(im) is np.ndarray) == False : print('file read error');exit()

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

print(f'contours count: {len(contours)} ')

#그리기 
cv.drawContours(im,
    contours, #윤각선 정보
    -1, #시작 인덱스 -1이면 모두그리기
    (0,255,0) #색
    ,3 #두께
)

# print(cv.imwrite('../output/contours1.png',im))

cv.imshow('temp',im)
cv.waitKey(0)
cv.destroyAllWindows()