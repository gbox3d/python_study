#%%
import os
import random
from IPython.core.display import display
import matplotlib.pyplot as plt
import PIL.Image as Image
from IPython.display import display

import time

import cv2
import numpy as np
from detectron2.utils.logger import setup_logger
import detectron2
import torch
import torchvision
import json

# check pytorch installation:
print(torch.__version__, torch.cuda.is_available())
# please manually install torch 1.9 if Colab changes its default version
assert torch.__version__.startswith("1.9")

# from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

from detectron2.utils.visualizer import Visualizer,ColorMode
from detectron2.engine import DefaultPredictor

import utils

#%% register dataset 
utils.register_Dataset(
        label_names = ['white-king', 'white-queen', 'white-bishop', 'white-knight', 'white-rook', 'white-pawn','black-king','black-queen', 'black-bishop', 'black-knight', 'black-rook', 'black-pawn','bishop'],
        dataset_name='chess'
    )
    
#%% 
ds_test = DatasetCatalog.get("chess_test")
_meta = MetadataCatalog.get("chess_test") # 메타데이터 추출 
print(_meta.thing_classes)

#%%
_d = ds_test[2]
img = cv2.imread(_d["file_name"])

#%% 라멜링확인 
visualizer = Visualizer(img[:, :, ::-1], 
    metadata=_meta, 
    # instance_mode=ColorMode.SEGMENTATION, # thing_colors로 지정해준 값을 사용하기 
    scale=1.0)
out = visualizer.draw_dataset_dict(_d) # 데이터셋 그리기 
display( Image.fromarray(out.get_image()))
# %%
config_path = './configs/chess/config.yaml'
cfg = get_cfg()
cfg.merge_from_file(config_path)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = './output/model_final.pth'
cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(_meta.thing_classes)
# instance segmentation predictor
predictor = DefaultPredictor(cfg)

#%%
start_tick = time.time()
outputs = predictor(img)
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), _meta, scale=1.0)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()))

