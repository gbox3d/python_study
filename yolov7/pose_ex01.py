#%%
# import argparse
import time
from pathlib import Path

import os
import copy
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

import sys

sys.path.append("../../yolov7")

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

from PIL import Image
from IPython.display import display

imgsz=640
half = True
# source  = '../../res/2022_10_25_17_43_47_dev_1.jpg'
weights = '../../yolov7/weights/yolov7-w6-pose.pt'
kpt_label = True
hide_labels = False
hide_conf = False

# Initialize
set_logging()
device = select_device('0')
half = device.type != 'cpu'

#%%
# Load model
model = attempt_load(weights, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride

imgsz = check_img_size(imgsz, s=stride)  # check img_size
names = model.module.names if hasattr(model, 'module') else model.names  # get class names
if half:
    model.half()  # to FP16

#%%
source = '../detectron2/sample/keypoint_detection/jua.jpg'
dataset = LoadImages(source, img_size=imgsz, stride=stride)
webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

#%%
# Run inference
if device.type != 'cpu':
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
# t0 = time.time()
for path, img, im0s, vid_cap in dataset:
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    # t1 = time_synchronized()
    pred = model(img, augment=False)[0]
    print(pred[...,4].max())
    
    # Apply NMS
    conf_thres = 0.45
    iou_thres = 0.25
    pred = non_max_suppression(pred, conf_thres, iou_thres,classes=None, agnostic=False, kpt_label=kpt_label)
    t2 = time_synchronized()
    
    for i, det in enumerate(pred):
        if webcam:  # batch_size >= 1
            p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
        else:
            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
        
        # print(det)
        if len(det):
            # Rescale boxes from img_size to im0 size
            scale_coords(img.shape[2:], det[:, :4], im0.shape, kpt_label=False)
            scale_coords(img.shape[2:], det[:, 6:], im0.shape, kpt_label=kpt_label, step=3)
            
            # Print results
            for c in det[:, 5].unique():
                n = (det[:, 5] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                
            for det_index, (*xyxy, conf, cls) in enumerate(reversed(det[:,:6])):
                c = int(cls)  # integer class
                label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                kpts = det[det_index, 6:]
                steps = 3
                num_kpts = len(kpts) // steps
                print(num_kpts)
                
                for kid in range(num_kpts):
                    # r, g, b = pose_kpt_color[kid]
                    x_coord, y_coord = kpts[steps * kid], kpts[steps * kid + 1]
                    
                    print(kid,int(x_coord), int(y_coord))
                    # 각부위별로 표시하기 
                    cv2.circle(im0, (int(x_coord), int(y_coord)), 3, (255,255,255), -1)
                    cv2.putText(im0,f'{kid}',(int(x_coord), int(y_coord)),3, 1,(255,0,0),1,cv2.LINE_AA)
                    
        display(Image.fromarray(cv2.cvtColor(im0,cv2.COLOR_BGR2RGB)))

# %%
