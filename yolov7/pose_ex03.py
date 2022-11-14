# 설명 :
# 이미지를 직접 읽어 변환시킨후 모델에 넣어 결과를 얻어보는 예제 
# 키포인트 중 손목 부분을 얻어 표시환다.

#%%
import cv2
import time
import torch
import argparse
import numpy as np

import sys
sys.path.append("../../yolov7")

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, set_logging,scale_coords,check_img_size
from utils.torch_utils import select_device


from PIL import Image
from IPython.display import display

print("torch version: ", torch.__version__)

def convert_yolov7_format(image,imgsz,stride):
    # Padded resize
    img = letterbox(image, imgsz, stride=stride, auto=False)[0]
    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img

#%%
imgsz=640
weights = '../../yolov7/weights/yolov7-w6-pose.pt'

#select device
device = select_device('0') # cpu or '0' ~ 'n' for gpu
half = device.type != 'cpu'
set_logging()

#%%# Load model
with torch.no_grad():
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride

    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    if half:
        model.half()  # to FP16

print('load model done')
print(f"model stride: {stride} , imgsz: {imgsz}")
print("name: ", names)

#%% load image
# source = '../detectron2/sample/keypoint_detection/jua.jpg'
orig_image = cv2.imread('../detectron2/sample/keypoint_detection/jua.jpg')
img = convert_yolov7_format(orig_image,imgsz,stride)

#%% 추론 
# gpu 일경우에 처리 
if device.type != 'cpu': 
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

pred = model(img, augment=False)[0]

# Apply NMS
conf_thres = 0.45
iou_thres = 0.25
pred = non_max_suppression(pred, 
                           conf_thres, 
                           iou_thres, 
                           classes=None, 
                           agnostic=False, 
                           kpt_label=True)
#%%
print("detection number ", len(pred[0][0]))

#%% 결과 확인
for i, det in enumerate(pred):
    im0 = orig_image.copy()
    if len(det):
        # Rescale boxes from img_size to im0 size
        # scale_coords(img.shape[2:], det[:, :4], im0.shape, kpt_label=False)
        scale_coords(img.shape[2:], det[:, 6:], im0.shape, kpt_label=True, step=3)
            
        for det_index, (*xyxy, conf, cls) in enumerate(reversed(det[:,:6])):
            c = int(cls)  # integer class
            kpts = det[det_index, 6:]
            steps = 3
            num_kpts = len(kpts) // steps
            print(num_kpts)
            
            left_wrist = ( int(kpts[steps* 9]), int(kpts[steps* 9 + 1]) ) # 왼 손목
            right_wrist = ( int(kpts[steps* 10]), int(kpts[steps* 10 + 1]) ) # 오른 손목
            
            left_elbow = ( int(kpts[steps* 7]), int(kpts[steps* 7 + 1]) ) # 왼 팔꿈치
            right_elbow = ( int(kpts[steps* 8]), int(kpts[steps* 8 + 1]) ) # 오른 팔꿈치
            
            print(left_wrist, right_wrist)
            
            cv2.circle(im0, left_wrist , 6, (255,0,0), -1)
            cv2.circle(im0, right_wrist , 6, (0,0,255), -1)
            
            cv2.line(im0, left_wrist, left_elbow, (255,0,0), 2)
            cv2.line(im0, right_wrist, right_elbow, (0,0,255), 2)
                
    display(Image.fromarray(cv2.cvtColor(im0,cv2.COLOR_BGR2RGB)))
# %%
