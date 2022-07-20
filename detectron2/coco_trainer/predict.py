#%%
from __future__ import annotations
import logging
import torch
from collections import OrderedDict
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances

from detectron2.data import (
    MetadataCatalog,
)

import time
import PIL.Image as Image
from IPython.display import display


import yaml

# from matplotlib import pyplot as plt
# from PIL import Image

#%%
with open('./settings.yaml') as f :
    _config = yaml.load(f, Loader=yaml.FullLoader)
    # print(_config)
    
register_coco_instances('test',{},
    _config['cfg']['test_set']['anno'],
    _config['cfg']['test_set']['img_dir'])

dataset_dicts = DatasetCatalog.get('test')
_metadata = MetadataCatalog.get('test')

print("Dataset loaded")

#%%
cfg = get_cfg()
cfg.merge_from_file( os.path.join(_config['cfg']['config_dir'], _config['dataset']['name']+ '_config.yaml'))
cfg.MODEL.WEIGHTS = os.path.join(_config['cfg']['output_dir'], "model_final.pth")  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
predictor = DefaultPredictor(cfg)

print("Predictor loaded")

#%%
_testData = dataset_dicts[0]


#%%
# instance_segmentation_predictor = DefaultPredictor(cfg)

#%%
img = cv2.imread(_testData['file_name'])

#%%
start_tick = time.time()
outputs = predictor(img)
print(f'delay { time.time() - start_tick }')
#%%
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
display( Image.fromarray(out.get_image()))
#%%
pred_classes = outputs["instances"].pred_classes.cpu().numpy()
pred_scores = outputs["instances"].scores.cpu().numpy()

print(pred_classes)
print(pred_scores)


# %%
