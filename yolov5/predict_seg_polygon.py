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

#%%
img = cv2.imread('./test1.jpg')  # BGR
np_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# display(Image.fromarray(np_img))
#%%

_model = Yolov5SegModel(weights='yolov5s-seg.pt', imgsz=(640, 640),device='' ,bs=1,dnn=False,half=False)

_,_,masks,segments,box_infos = _model.predict(img)

#%%
for box_info in box_infos:
    print('box :', box_info[0].item(), box_info[1].item(), box_info[2].item(), box_info[3].item())
    print('conf :', box_info[4].item())
    print('class :', _model.names[ int(box_info[5].item())] )

#%%
im0 = img.copy()
out_img = im0.copy()
for i in range(len(masks)):

    seg = segments[i].reshape(-1)  # (n,2) to (n*2)

    _seg = seg.copy()

    for i in range( int(len(_seg) /2) ):
        _seg[i*2] = _seg[i*2] * im0.shape[1]
        _seg[i*2+1] = _seg[i*2+1] * im0.shape[0]
        
    
    np_cnt = np.asarray(_seg,dtype=np.int32).reshape(-1,1,2)
    out_img = cv2.polylines(out_img, [np_cnt], True, (0,255,0), 2)
    out_img = cv2.cvtColor(out_img,cv2.COLOR_BGR2RGB)


display(Image.fromarray(out_img))
