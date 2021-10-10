#%%
import os
import random
from IPython.core.display import display
import matplotlib.pyplot as plt
import PIL.Image as Image
from IPython.display import display

import cv2
import numpy as np
from detectron2.utils.logger import setup_logger
import detectron2
import torch
import torchvision

# check pytorch installation:
print(torch.__version__, torch.cuda.is_available())
# please manually install torch 1.9 if Colab changes its default version
assert torch.__version__.startswith("1.9")

from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

from detectron2.utils.visualizer import Visualizer
from detectron2.engine import DefaultPredictor


#%%
register_coco_instances("microcontroller_test",{},
"../../datasets/Microcontroller Segmentation/test.json",
"../../datasets/Microcontroller Segmentation/test"
)

#%%
dataset_dicts = DatasetCatalog.get("microcontroller_test")
print(dataset_dicts[0])
ds_item = dataset_dicts[0]
# print(ds_item["file_name"])

im = cv2.imread(ds_item["file_name"])
display( Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)))


# %%
_meta = MetadataCatalog.get("microcontroller_test")
# print(_meta)
print( f'type : {_meta.evaluator_type}' )
print(f'image root : {_meta.image_root}')
print(f'json file path : {_meta.json_file}')
print(f'class list :  {_meta.thing_classes}')
print(f'name : {_meta.name}')

# %%
