#%% video sample for mp4
import os
import io
import cv2 as cv 
import numpy as np
import yaml
import time

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display
print( f"opencv version : {cv.__version__}")

with open('./config.yaml') as f :
    _config = yaml.load(f, Loader=yaml.FullLoader)

url = _config['test']['vid_src']
print(url)

#%%
cap = cv.VideoCapture(url)
cap.set(cv.CAP_PROP_BUFFERSIZE,1)
print( f'fps {cap.get(cv.CAP_PROP_FPS)}')
fps = cap.get(cv.CAP_PROP_FPS)

t0 = time.time()
#%%
if cap.isOpened():
    print(f'connect stream : {url}')
    #해상도 얻기
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    count = 0

    while cap.isOpened():
        
        delay = time.time() - t0
        t0 = time.time()
        # print(delay)

        # _frame_skip =  int(fps * delay * 1.5) 
        _frame_skip = 1
        print(f'frame skip {_frame_skip}')

        for i in range( _frame_skip ) :
            cap.grab()
        ret, frame = cap.read()
        display(Image.fromarray(cv.cvtColor(frame,cv.COLOR_BGR2RGB)))
        time.sleep(5)
        
        count += 1
        if count > 5 : 
            cap.release()
            break;

else :
    print('connect failed')
#%%
