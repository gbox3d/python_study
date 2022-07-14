#%%
import os
# import random
import yaml
import matplotlib.pyplot as plt
# import cv2
# import numpy as np
from detectron2.utils.logger import setup_logger
# import detectron2
import torch
# import torchvision

# check pytorch installation:
print(torch.__version__, torch.cuda.is_available())
# please manually install torch 1.9 if Colab changes its default version
# assert torch.__version__.startswith("1.9")

from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
# from detectron2.data import DatasetCatalog, MetadataCatalog
# from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo

#%%
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("microcontroller_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.SOLVER.IMS_PER_BATCH = 32
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = 1000
cfg.SOLVER.STEPS = []        # do not decay learning rate
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

# 설정 파일 덤프 하고 astrophysics.yaml 로 저장 
cfg_file = yaml.safe_load(cfg.dump())

print(cfg_file)

# %%

with open('configs/microcontroller_config.yaml', 'w') as f:
    yaml.dump(cfg_file, f)

# %%
