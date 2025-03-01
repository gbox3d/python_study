#%%
import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

# FILE = Path(__file__).resolve()
# ROOT = FILE.parents[0]  # YOLOv5 root directory
# if str(ROOT) not in sys.path:
#     sys.path.append(str(ROOT))  # add ROOT to PATH
# ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def loadModel(yolov5_path):
    sys.path.append(yolov5_path)
    
    # from models.common import DetectMultiBackend
    # from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
    # from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
    #                         increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
    # from utils.plots import Annotator, colors, save_one_box
    # from utils.torch_utils import select_device, time_sync
    
    from models.common import DetectMultiBackend
    from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
    from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                            increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
    from utils.plots import Annotator, colors, save_one_box
    from utils.torch_utils import select_device, smart_inference_mode
    
    print('ok')
