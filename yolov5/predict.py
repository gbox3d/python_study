#%%
import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn


from yolov5lib import loadModel

# FILE = Path(__file__).resolve()
# ROOT = FILE.parents[0]  # YOLOv5 root directory
# if str(ROOT) not in sys.path:
#     sys.path.append(str(ROOT))  # add ROOT to PATH
# ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# sys.path.append('/home/gbox3d/work/visionApp/yolov5')

# #%%
# from models.common import DetectMultiBackend
# from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
# from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
#                            increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
# from utils.plots import Annotator, colors, save_one_box
# from utils.torch_utils import select_device, time_sync
# # %%
# print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

# #%%
# device=0 # cuda device, i.e. 0 or 0,1,2,3 or cpu
# device = select_device(device)
# model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)
# stride, names, pt, jit, onnx, engine = model.stride, model.names, model.pt, model.jit, model.onnx, model.engine
# imgsz = check_img_size(imgsz, s=stride)  # check image size
#%%
loadModel(
    yolov5_path='/home/gbox3d/work/visionApp/yolov5'
)
# %%
