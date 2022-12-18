#%%
from mss import mss,tools
import cv2
import numpy as np
from PIL import Image
from IPython.display import display

#%%
with mss() as sct:
    
    monitor = {"top": 0, "left": 0, "width": 320, "height": 200}
    while True:
        img = sct.grab(monitor)
        
        np_img = np.array(img)
        cv2.imshow('capture',np_img)
        
        if cv2.waitKey(20) & 0xff == 27 : # esc key exit
            cv2.destroyAllWindows()
            break;
    
    