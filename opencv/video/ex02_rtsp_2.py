#%% video sample for mp4
import cv2 as cv
import numpy as np


from PIL import Image
from IPython.display import display

from IPython.display import display
print( f"opencv version : {cv.__version__}")

#%%
url = f'rtsp://192.168.4.62:554/stream_ch00_0' # fxt

#%%
cap = cv.VideoCapture(url)
if cap.isOpened() :
    print(f'open success {url}')
    ret, frame = cap.read()
    if ret is True:
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        display( Image.fromarray(img_rgb) )
    else :
        print('capture failed')
    cap.release()


# %%
