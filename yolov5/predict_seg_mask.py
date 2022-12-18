#%%

import torch
import numpy as np
import cv2

from yolov5SegModel import Yolov5SegModel

from IPython.display import display
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageColor as ImageColor
import PIL.Image as Image

img = cv2.imread('bus.jpg')  # BGR
np_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# display(Image.fromarray(np_img))
#%%
_model = Yolov5SegModel(weights='yolov5m-seg.pt', imgsz=(640, 640),device='' ,bs=1,dnn=False,half=False)

_,_,masks,segments,box_infos = _model.predict(img)

if masks is None:
    print('no object found')
    exit()    

#%%
im0 = np_img.copy()
out_img = im0.copy()

for index,box_info in enumerate(box_infos):
    print('box :', box_info[0].item(), box_info[1].item(), box_info[2].item(), box_info[3].item())
    print('conf :', box_info[4].item())
    print('class :', _model.names[ int(box_info[5].item())] )
    
#%%
#resize 640x640 to 640x480
out_img = cv2.resize(out_img,masks[0].shape[:2][::-1])
total_np_mask_img = np.zeros(masks[0].shape,dtype=np.uint8)

if masks is not None:   
    for i in range(len(masks)):
        mask = masks[i]
        _box = box_infos[i]
        
        if _box[5].item() == 0: # collect person mask
            np_mask_img = np.asarray((mask)*255,dtype=np.uint8)
            # display(Image.fromarray(np_mask_img))
            total_np_mask_img = cv2.bitwise_or(total_np_mask_img,np_mask_img)
        
        
display(Image.fromarray(total_np_mask_img))  
      
# out_img = cv2.bitwise_and(out_img,out_img,mask=total_np_mask_img) # apply mask
# display(Image.fromarray(out_img))
        
# %%
_total_np_mask_img = cv2.cvtColor(total_np_mask_img, cv2.COLOR_GRAY2BGRA)
_total_np_mask_img[:,:,3] = total_np_mask_img #alpha channel

display(Image.fromarray(_total_np_mask_img))

# _total_np_mask_img[ total_np_mask_img[:] ] = [0,0,0,255]

_out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2BGRA)
_out_img[:,:,3] = 255

_out_img = cv2.bitwise_and(_out_img,_total_np_mask_img) # apply mask
display(Image.fromarray(_out_img))

# %%
