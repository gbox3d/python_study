#%%
import cv2 as cv
import numpy as np
from PIL import Image
from IPython.display import display

#%%
img = cv.imread("../../res/shally.jpg", cv.IMREAD_GRAYSCALE)
src = cv.cuda_GpuMat()
src.upload(img)

clahe = cv.cuda.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
dst = clahe.apply(src, cv.cuda_Stream.Null())

result = dst.download()

img_rgb = cv.cvtColor(result, cv.COLOR_BGR2RGB)

display( Image.fromarray(img_rgb) )

# cv2.imshow("result", result)
# cv2.waitKey(0)
# %%
