#%%
import os
from unicodedata import category
import cv2
import numpy as np

#import the COCO Evaluator to use the COCO Metrics
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import build_detection_test_loader
from detectron2.data.datasets import register_coco_instances
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import MetadataCatalog,DatasetCatalog
from detectron2 import model_zoo

#%%
weight_path = './output' 
# %%
for d in ["train", "test"]:
    register_coco_instances(
        f"microcontroller_{d}", 
        {},
        f"../../datasets/Microcontroller Segmentation/{d}.json",
        f"../../datasets/Microcontroller Segmentation/{d}"
    )
#%%
cfg_instance_seg = get_cfg()
# cfg_instance_seg.merge_from_file(os.path.join(weight_path,'config.yaml'))
cfg_instance_seg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg_instance_seg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_instance_seg.MODEL.WEIGHTS =  os.path.join(weight_path,'model_final.pth') #f'./output/{dataset_name}/model_final.pth'

cfg = cfg_instance_seg
# Create predictor
predictor = DefaultPredictor(cfg)

#%%
evaluator = COCOEvaluator("microcontroller_test", cfg, False, output_dir="./output/")
val_loader = build_detection_test_loader(cfg, "microcontroller_test")

#Use the created predicted model in the previous step
inference_on_dataset(predictor.model, val_loader, evaluator)


# %%
