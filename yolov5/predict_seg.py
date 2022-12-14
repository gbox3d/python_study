#%%
import argparse
import os
import platform
import sys
from pathlib import Path

import torch
import numpy as np

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, scale_segments,
                           strip_optimizer)
from utils.plots import Annotator, colors, save_one_box
from utils.segment.general import masks2segments, process_mask, process_mask_native
from utils.torch_utils import select_device, smart_inference_mode

from utils.augmentations import (Albumentations, augment_hsv, classify_albumentations, classify_transforms, copy_paste,
                                 letterbox, mixup, random_perspective)


from IPython.display import display
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageColor as ImageColor
import PIL.Image as Image

#%%
img = cv2.imread('./test1.jpg')  # BGR
# img = cv2.imread('./2022_12_12_14_42_57_dev_9610763.jpg')  # BGR
# img = cv2.imread('./bus.jpg')  # BGR
np_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
display(Image.fromarray(np_img))

# %%

imgsz=(640, 640)  # inference size (height, width)
conf_thres=0.25  # confidence threshold
iou_thres=0.45  # NMS IOU threshold
max_det=1000  # maximum detections per image
device=''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
view_img=False  # show results
save_txt=False  # save results to *.txt
save_conf=False  # save confidences in --save-txt labels
save_crop=False  # save cropped prediction boxes
nosave=False  # do not save images/videos
classes=None  # filter by class: --class 0, or --class 0 2 3
agnostic_nms=False  # class-agnostic NMS
augment=False  # augmented inference
visualize=False  # visualize features
update=False  # update all models
name='exp'  # save results to project/name
exist_ok=False  # existing project/name ok, do not increment
line_thickness=3  # bounding box thickness (pixels)
hide_labels=False  # hide labels
hide_conf=False  # hide confidences
half=False  # use FP16 half-precision inference
dnn=False  # use OpenCV DNN for ONNX inference
vid_stride=1  # video frame-rate stride
retina_masks=False

# %%
# Load model

device = select_device('') # CUDA:0,1,2,3 or CPU
# model = DetectMultiBackend('yolov5s-seg.pt', device=device, dnn=dnn, fp16=half)
model = DetectMultiBackend('hhgun_s.pt', device=device, dnn=dnn, fp16=half)
stride, names, pt = model.stride, model.names, model.pt

imgsz = check_img_size(imgsz, s=stride)  # check image size


# %%
print(model.device)
print(stride,pt,names)
# %%
im0 = img.copy()
im = letterbox(im0, 640, stride=stride, auto=True)[0]  # padded resize
# display(Image.fromarray(im))
im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
im = np.ascontiguousarray(im)  # contiguous
# %%
im = torch.from_numpy(im).to(model.device)
im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
im /= 255  # 0 - 255 to 0.0 - 1.0
if len(im.shape) == 3:
    im = im[None]  # expand for batch dim


# %%
bs=1
model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
pred, proto = model(im, augment=False, visualize=False)[:2]
pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det, nm=32)

# print(pred)

#%%
masks = None
for i, det in enumerate(pred):  # per image
    # print(i,det)
    if(len(det) > 0):
        masks = process_mask(proto[i], det[:, 6:], det[:, :4], im.shape[2:], upsample=True)  # HWC
        det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()  # rescale boxes to im0 size
        
        segments = [
            scale_segments(im0.shape if retina_masks else im.shape[2:], x, im0.shape, normalize=True)
            for x in reversed(masks2segments(masks))
            ]
        # mask = masks[i]
        for j, (*xyxy, conf, cls) in enumerate(reversed(det[:, :6])):
            # print(cls,conf)
            seg = segments[j].reshape(-1)  # (n,2) to (n*2)
            print(seg.shape)
            line = (cls, *seg, conf)
        
#%% draw mask
if masks is not None:
    for i in range(len(masks)):
        mask = masks[i]
        print(mask.shape)
        display(Image.fromarray(np.asarray((mask)*255,dtype=np.uint8)))
else :
    print("no mask")

#%%
# for i in range(len(masks)):
print(len(seg))
#%%
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

# %%
