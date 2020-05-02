# region of images
import numpy as np
import cv2 as cv

img = cv.imread('../res/messi5.jpg')
ball = img[280:340,330:390]
img[273:333, 100:160] = ball

#save result
cv.imwrite('../output/test.png',img)