#%%
import torch

import io
import numpy as np
from pathlib import Path
import base64


import cv2

from IPython.display import display
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageColor as ImageColor
import PIL.Image as Image
#%% load test image
img = cv2.imread('./bus.jpg')  # BGR
np_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
display(Image.fromarray(np_img))
# %%
model = torch.hub.load(
    '/home/gbox3d/work/visionApp/yolov5',
    'custom',
    path='./yolov5s.pt',
    source='local'
    )

#%%
# model.conf = 0.25  # NMS confidence threshold
#     iou = 0.45  # NMS IoU threshold
#     agnostic = False  # NMS class-agnostic
#     multi_label = False  # NMS multiple labels per box
#     classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
#     max_det = 1000  # maximum number of detections per image
#     amp = False  # Automatic Mixed Precision (AMP) inference

# Inference
results = model(
    np_img.copy(),
    size=1280, # 실제 추론에 입력될 이미지 크기, 크기가 클수록 느리지만 정확해지고 작을수록 빠르지만 정확하지 않음 ,320,640 과 비교
    )
results.print()

#%% 결과를 이미지로 랜더링하기
results.render()
for img in results.imgs:
    buffered = io.BytesIO() # 인코딩 결과를 넣을 빈버퍼 선언 
    img_base64 = Image.fromarray(img)
    display(img_base64)
    # jpg 형식으로 인코딩 하고 buffered에 저장
    img_base64.save(buffered, format="JPEG")
    
    with open('./test.jpg','wb') as fd :
        fd.write( buffered.getvalue() ) # save encoded jpeg buffer to file

    
    print(base64.b64encode(buffered.getvalue()).decode('utf-8')) 

# %%
xyxy_pred = results.xyxy[0]
print( f'pref shape {xyxy_pred.shape}' )

for *box, conf, cls in reversed(xyxy_pred):
    xmin = int(box[0])
    ymin = int(box[1])
    xmax = int(box[2])
    ymax = int(box[3])
    print(xmin,ymin,xmax,ymax , float(conf), int(cls))

# %%
