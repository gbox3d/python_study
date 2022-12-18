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
for box_info in box_infos:
    print('box :', box_info[0].item(), box_info[1].item(), box_info[2].item(), box_info[3].item())
    print('conf :', box_info[4].item())
    print('class :', _model.names[ int(box_info[5].item())] )
    
#%%
im0 = np_img.copy()
out_img = im0.copy()
if masks is not None:
                
    for i in range(len(masks)):
        mask = masks[i]
        _seg = segments[i]
        
        # seg_poly = Polygon(_seg)
        # print('seg_poly' , seg_poly.area)
        
        np_mask_img = np.asarray((mask)*255,dtype=np.uint8)
        out_img = cv2.bitwise_and(out_img,out_img,mask=np_mask_img)
        
display(Image.fromarray(np_mask_img))
        
        



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
    
    rect = cv2.minAreaRect(np_cnt)
    box = cv2.boxPoints(rect)
    cv2.drawContours(out_img, [np.int0(box)], 0, (255,0,0), 2)
    
    print('box :', box)
    
    _rear = [int( (box[0][0] + box[1][0]) /2 ), int( (box[0][1] + box[1][1]) /2 )]
    _front = [int( (box[2][0] + box[3][0]) /2 ), int( (box[2][1] + box[3][1]) /2 )]
    
    # cv2.circle(out_img, tuple(_rear), 5, (0,255,0), -1)
    # cv2.circle(out_img, tuple(_front), 5, (0,255,0), -1)
    
    _dist = np.linalg.norm(np.array(_rear) - np.array(_front))
    
    _rear2 = [int( (box[0][0] + box[3][0]) /2 ), int( (box[0][1] + box[3][1]) /2 )]
    _front2 = [int( (box[1][0] + box[2][0]) /2 ), int( (box[1][1] + box[2][1]) /2 )]
    
    # cv2.circle(out_img, tuple(_rear2), 5, (255,0,0), -1)
    # cv2.circle(out_img, tuple(_front2), 5, (255,0,0), -1)
    
    _dist2 = np.linalg.norm(np.array(_rear2) - np.array(_front2))
    
    print('dist :', _dist, _dist2)
    
    if(_dist > _dist2): 
        if _rear[1] > _front[1] :
            _temp = _rear
            _rear = _front
            _front = _temp
            
        result = [_rear,_front,_dist]
    else:
        if _rear2[1] > _front2[1] :
            _temp = _rear2
            _rear2 = _front2
            _front2 = _temp
        result = [_rear2,_front2,_dist2]
        
    cv2.circle(out_img, tuple(result[0]), 5, (0,255,0), -1) # rear
    cv2.circle(out_img, tuple(result[1]), 5, (255,255,0), -1) # front
    

display(Image.fromarray(out_img))

# %%
