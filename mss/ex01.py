#%%
from mss import mss,tools
import cv2
import numpy as np
from PIL import Image
from IPython.display import display

# import mss.tools


#%%
with mss() as sct:
    filename = sct.shot()
    print(filename)
    
# %%
with mss() as sct:
    # monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
    # Grab the data
    sct_img = sct.grab(sct.monitors[0])
    display( Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX") )
    
    _png = tools.to_png(sct_img.rgb, sct_img.size, output="sct.png")
    
    
    
# %% png -> opencv
with mss() as sct:
    monitor = {"top": 160, "left": 160, "width": 640, "height": 480}
    sct_img = sct.grab(monitor)
    _png = tools.to_png(sct_img.rgb, sct_img.size)
    img_np = cv2.imdecode(np.fromstring(_png, np.uint8), cv2.IMREAD_COLOR)
    display( Image.fromarray(img_np) )
    
# %%
with mss() as sct:
    img = sct.grab(sct.monitors[0])
    np_img = np.array(img)
    display( Image.fromarray(np_img) )

# %%
