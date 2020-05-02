import numpy as np
import cv2 as cv
import sys

img = cv.imread('../../res/messi5.jpg')

# print(type(img) is np.ndarray )

if (type(img) is np.ndarray) == False : 
    print('file read failed')
    sys.exit()

print("-------read [100,100] BGR-------------")
px = img[100,100]
print(px)
#read pixel
print(px[0])
print(px[1])
print(px[2])


print("-------read [100,100,x] BGR-------------")

print('B',img[100,100,0])
print('G',img[100,100,1])
print('R',img[100,100,2])

print("-----image info---------------")
# get image info
print('shap : ', img.shape)
print('size : ' , img.size)
print('data type : ' , img.dtype)
print('type : ' , type(img))

#write pixel

for x in range(100) :
    for y in range(50) :
        img[100 + y,100+x] = [0,0,255]

#save result
cv.imshow("result",img)
cv.waitKey(0)
cv.destroyAllWindows()
# cv.imwrite('../output/test.png',img)



