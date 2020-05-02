import numpy as np
import cv2 as cv

img = cv.imread('../res/contour1.png')

cv.imshow('img', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = np.float32(gray)

##해리스 코너 
dst = cv.cornerHarris(gray, 2, 3, 0.04)

dst = cv.dilate(dst, None)

print(type(dst))

img[dst > 0.01 * dst.max()] = [0, 0, 255]

cv.imshow('dst', img)

## 시토마시 코너 
corners = cv.goodFeaturesToTrack(gray, 100, 0.01, 10)

corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv.circle(img, (x, y), 3, [255, 255, 0], -1)

cv.imshow('Shi-Tomasi Corner Detector', img)


if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()