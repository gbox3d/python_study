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

#%%
utils.loadCocoDataset(
    dataset_path = '../../../../datasets',
    dataset_name = 'AmericanMushromms')

# %%
config_path = './configs/AmericanMushromms/config.yaml'
cfg = get_cfg()
cfg.merge_from_file(config_path)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = './output/AmericanMushromms/model_final.pth'


#%%
import argparse
import os
import onnx

from detectron2.checkpoint import DetectionCheckpointer
from detectron2.data import build_detection_test_loader
from detectron2.modeling import build_model
from detectron2.export import Caffe2Tracer

output = "output/export_models"

os.makedirs(output, exist_ok=True)

# create a torch model
torch_model = build_model(cfg)
DetectionCheckpointer(torch_model).resume_or_load(cfg.MODEL.WEIGHTS)

# get a sample data

data_loader = build_detection_test_loader(cfg, cfg.DATASETS.TEST[0])
first_batch = next(iter(data_loader))

#%%

inputs = [{"image": first_batch[0]['image']}]

#%%
tracer = Caffe2Tracer(cfg, torch_model, first_batch)

# convert and save caffe2 model
caffe2_model = tracer.export_caffe2()
caffe2_model.save_protobuf(output)
# draw the caffe2 graph
caffe2_model.save_graph(os.path.join(output, "model.svg"), inputs=first_batch)

#%%
from detectron2.export import Caffe2Model

model = Caffe2Model.load_protobuf(output)
# %%
import torch
torch.cuda.empty_cache()

im = first_batch[0]['image']

inputs = [{"image": im}]
outputs = model(inputs)
# %%
