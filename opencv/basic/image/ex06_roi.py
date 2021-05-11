#%% region of images
import numpy as np
import cv2 as cv

from PIL import Image
from IPython.display import display
import pathlib

#%%
img = cv.imread('../../res/messi5.jpg')

display(Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)))

#%% crop and paste
ball = img[280:340,330:390]
img[273:333, 100:160] = ball
display(Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)))

#%%
#save result
cv.imwrite('../output/test.png',img)