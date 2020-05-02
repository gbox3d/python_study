import numpy as np
import cv2 as cv
# Load an color image in grayscale
img = cv.imread('./res/contour1.png',0) 

print(type(img))
# print(img[0])

cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.imshow('image',img)
# cv.waitKey(0)

k = cv.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv.imwrite('messigray.png',img)
    cv.destroyAllWindows()

cv.destroyAllWindows()
