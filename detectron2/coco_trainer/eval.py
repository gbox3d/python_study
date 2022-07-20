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
from detectron2.engine import DefaultTrainer
from detectron2.utils.visualizer import ColorMode
from detectron2.solver import build_lr_scheduler, build_optimizer
from detectron2.checkpoint import DetectionCheckpointer, PeriodicCheckpointer
from detectron2.utils.events import EventStorage
from detectron2.modeling import build_model
import detectron2.utils.comm as comm
from detectron2.engine import default_argument_parser, default_setup, default_writers, launch
from detectron2.data import (
    MetadataCatalog,
    build_detection_test_loader,
    build_detection_train_loader,
)
from detectron2.evaluation import (
    CityscapesInstanceEvaluator,
    CityscapesSemSegEvaluator,
    COCOEvaluator,
    COCOPanopticEvaluator,
    DatasetEvaluators,
    LVISEvaluator,
    PascalVOCDetectionEvaluator,
    SemSegEvaluator,
    inference_on_dataset,
    print_csv_format,
)


import yaml

# from matplotlib import pyplot as plt
# from PIL import Image

settgins_file = './settings.yaml'
#%%
import argparse
parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument(
    '-s','--settings', type=str, 
    default='./settings.yaml',
    help='choose  your settings file')

settgins_file = parser.parse_args().settings


#%%

with open(settgins_file) as f :
    _config = yaml.load(f, Loader=yaml.FullLoader)
    print(_config)

# %%
#load dataset
# VERSION = 2
# from roboflow import Roboflow
# rf = Roboflow(api_key="-------")
# project = rf.workspace("team-roboflow").project("american-sign-language-poly")
# dataset = project.version(VERSION).download("coco")

# register_coco_instances("asl_poly_train", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/train/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/train/")
# register_coco_instances("asl_poly_valid", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/valid/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/valid/")
# register_coco_instances("asl_poly_test", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/test/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/test/")

register_coco_instances('test',{},
    _config['eval']['anno'],
    _config['eval']['img_dir'])

print("Dataset loaded")

#%%
cfg = get_cfg()
cfg.merge_from_file( _config['eval']['config'] )
# cfg = get_cfg()
# # cfg.DATASETS.TEST = ("asl_poly_test",)#Test dataset registered in a previous cell
# cfg.merge_from_file()
cfg.MODEL.WEIGHTS = _config['eval']['weight']  # path to the model we just trained
# cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2   # set a custom testing threshold
# cfg.MODEL.ROI_HEADS.NUM_CLASSES = 27
# cfg.OUTPUT_DIR = "./output"
predictor = DefaultPredictor(cfg)
# model = build_model(cfg)

evaluator = COCOEvaluator("test", cfg, False, output_dir="./output/")
val_loader = build_detection_test_loader(cfg, "test")

#Use the created predicted model in the previous step
result_i = inference_on_dataset(predictor.model, val_loader, evaluator)


#%%
print(result_i)
