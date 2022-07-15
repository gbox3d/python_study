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

from roboflow import Roboflow

from matplotlib import pyplot as plt
from PIL import Image
# %%
#load dataset
VERSION = 2
# rf = Roboflow(api_key="-------")
# project = rf.workspace("team-roboflow").project("american-sign-language-poly")
# dataset = project.version(VERSION).download("coco")

# register_coco_instances("asl_poly_train", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/train/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/train/")
# register_coco_instances("asl_poly_valid", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/valid/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/valid/")
register_coco_instances("asl_poly_test", {}, f"./dataset/American-Sign-Language-Poly-{VERSION}/test/_annotations.coco.json", f"./dataset/American-Sign-Language-Poly-{VERSION}/test/")

print("Dataset loaded")

#%%
#test module
def get_evaluator(cfg, dataset_name, output_folder=None):
    """
    Create evaluator(s) for a given dataset.
    This uses the special metadata "evaluator_type" associated with each builtin dataset.
    For your own dataset, you can simply create an evaluator manually in your
    script and do not have to worry about the hacky if-else logic here.
    """
    if output_folder is None:
        output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
    evaluator_list = []
    evaluator_type = MetadataCatalog.get(dataset_name).evaluator_type
    if evaluator_type in ["sem_seg", "coco_panoptic_seg"]:
        evaluator_list.append(
            SemSegEvaluator(
                dataset_name,
                distributed=True,
                output_dir=output_folder,
            )
        )
    if evaluator_type in ["coco", "coco_panoptic_seg"]:
        evaluator_list.append(COCOEvaluator(dataset_name, output_dir=output_folder))
    if evaluator_type == "coco_panoptic_seg":
        evaluator_list.append(COCOPanopticEvaluator(dataset_name, output_folder))
    if evaluator_type == "cityscapes_instance":
        return CityscapesInstanceEvaluator(dataset_name)
    if evaluator_type == "cityscapes_sem_seg":
        return CityscapesSemSegEvaluator(dataset_name)
    if evaluator_type == "pascal_voc":
        return PascalVOCDetectionEvaluator(dataset_name)
    if evaluator_type == "lvis":
        return LVISEvaluator(dataset_name, cfg, True, output_folder)
    if len(evaluator_list) == 0:
        raise NotImplementedError(
            "no Evaluator for the dataset {} with the type {}".format(dataset_name, evaluator_type)
        )
    if len(evaluator_list) == 1:
        return evaluator_list[0]
    return DatasetEvaluators(evaluator_list)

logger = logging.getLogger("detectron2")

def do_test(cfg, model):
    results = OrderedDict()
    for dataset_name in cfg.DATASETS.TEST:
        data_loader = build_detection_test_loader(cfg, dataset_name)
        evaluator = get_evaluator(
            cfg, dataset_name, os.path.join(cfg.OUTPUT_DIR, "inference", dataset_name)
        )
        results_i = inference_on_dataset(model, data_loader, evaluator)
        results[dataset_name] = results_i
        if comm.is_main_process():
            logger.info("Evaluation results for {} in csv format:".format(dataset_name))
            print_csv_format(results_i)
    if len(results) == 1:
        results = list(results.values())[0]
    return results

#%%
cfg = get_cfg()
# cfg.DATASETS.TEST = ("asl_poly_test",)#Test dataset registered in a previous cell
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = os.path.join("./output/", "model_final.pth")  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2   # set a custom testing threshold
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 27
cfg.OUTPUT_DIR = "./output"
predictor = DefaultPredictor(cfg)
# model = build_model(cfg)

#%%
# do_test(cfg, model)
# results = OrderedDict()
# dataset_name = 'asl_poly_test'
# data_loader = build_detection_test_loader(cfg, dataset_name)
# evaluator = get_evaluator(
#             cfg, dataset_name, os.path.join(cfg.OUTPUT_DIR, "inference", dataset_name)
#         )
# results_i = inference_on_dataset(predictor.model, data_loader, evaluator)
# results[dataset_name] = results_i

# %%
evaluator = COCOEvaluator("asl_poly_test", cfg, False, output_dir="./output/")
val_loader = build_detection_test_loader(cfg, "asl_poly_test")

#Use the created predicted model in the previous step
inference_on_dataset(predictor.model, val_loader, evaluator)

# %%
