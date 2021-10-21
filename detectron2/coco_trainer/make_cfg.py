#%%
import os
from detectron2 import config
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
assert torch.__version__.startswith("1.9")

from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
# from detectron2.data import DatasetCatalog, MetadataCatalog
# from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import utils
#%%
base_config_file = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
config_dir = './configs/AmericanMushromms'
output_dir = './output/AmericanMushromms'
datasetname = 'AmericanMushromms'
MAX_ITER = 5000
IMS_PER_BATCH = 2

config_name = 'config.yaml'
config_path = os.path.join(config_dir,config_name)

#%%
utils.loadCocoDataset(
    dataset_path = '../../../../datasets',
    dataset_name = datasetname)
ds_test = DatasetCatalog.get(f"{datasetname}_test")
_meta = MetadataCatalog.get(f"{datasetname}_test") # 메타데이터 추출 
print(_meta.thing_classes)
print(f'class num : {len(_meta.thing_classes)}')
NUM_CLASSES = len(_meta.thing_classes)


#%%
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(base_config_file))
cfg.DATASETS.TRAIN = (datasetname+'_train',datasetname+'_valid')
cfg.DATASETS.TEST = (datasetname+'_test',)
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(base_config_file)
cfg.SOLVER.IMS_PER_BATCH = IMS_PER_BATCH
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = MAX_ITER
cfg.SOLVER.STEPS = []        # do not decay learning rate

cfg.OUTPUT_DIR = output_dir
cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES

cfg.TEST.AUG.ENABLED = True
cfg.TEST.EVAL_PERIOD = 100

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)

# 설정 파일 덤프 하고 astrophysics.yaml 로 저장 
cfg_file = yaml.safe_load(cfg.dump())
with open(config_path, 'w') as f:
    yaml.dump(cfg_file, f)
print(f'{config_path}  done')
# %%
