#%%
import torch
# import torchvision
import cv2
print(f'torch : {torch.__version__}' )
print(f'cuda : {torch.cuda.is_available()}')
print(f'cv version : {cv2.__version__}')


#%%
import time
import PIL.Image as Image
from IPython.display import display


# Setup detectron2 logger
import detectron2
# from detectron2.utils.logger import setup_logger
# setup_logger()

# import some common libraries
import numpy as np

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

print(f'detectron : {detectron2.__version__}')
#%% object detection
img = cv2.imread("../res/input.jpg")
print(img.shape)
 # %%
# creating detectron2 config https://github.com/facebookresearch/detectron2/blob/master/MODEL_ZOO.md
cfg_object_detection = get_cfg()
cfg_object_detection.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
cfg_object_detection.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_object_detection.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

# object detection predictor
object_detection_predictor = DefaultPredictor(cfg_object_detection)

start_tick = time.time()
outputs = object_detection_predictor(img)
# using `Visualizer` to draw the predictions on the image.
v = Visualizer(cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(cfg_object_detection.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()) )


#%% instance segmentation
# create config for instance segmentation
cfg_instance_seg = get_cfg()
cfg_instance_seg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg_instance_seg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_instance_seg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")


# instance segmentation predictor
instance_segmentation_predictor = DefaultPredictor(cfg_instance_seg)

start_tick = time.time()
outputs = instance_segmentation_predictor(img)
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(cfg_instance_seg.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()))

# %% key point
# create config for Keypoints detection
cfg_keypoints = get_cfg()
cfg_keypoints.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
cfg_keypoints.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_keypoints.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")

# Keypoints predictor
keypoints_predictor = DefaultPredictor(cfg_keypoints)

start_tick = time.time()
outputs = keypoints_predictor(img)
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(cfg_keypoints.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()))

# %%
# create config for Panoptic segmentation
cfg_panoptic = get_cfg()
cfg_panoptic.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
cfg_panoptic.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")

# Panoptic segmentation predictor
panoptic_predictor = DefaultPredictor(cfg_panoptic)
start_tick = time.time()
panoptic_seg, segments_info = panoptic_predictor(img)["panoptic_seg"]
# using `Visualizer` to draw the predictions on the image.
v = Visualizer(cv2.cvtColor(img,cv2.COLOR_BGR2RGB) , MetadataCatalog.get(cfg_panoptic.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_panoptic_seg_predictions(panoptic_seg.to("cpu"), segments_info)
print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()))

# %%
