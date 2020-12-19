#%% output cv to pil
import cv2 as cv
import numpy as np
from PIL import Image
from IPython.display import display
import pathlib

print( "opencv version :" + cv.__version__)
print(pathlib.Path.cwd())

#%%비트멥 만들기 
img = np.zeros((512,512,3),np.uint8)

#텍스트 출력 
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV ',(10,500), font, 0.5,(0,0,255),2,cv.LINE_AA)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

display( Image.fromarray(img_rgb) )
# %%
