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
img = cv2.imread("./jua.jpg")
# img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
print(img.shape)
 
# %% key point
# create config for Keypoints detection
_cfg = get_cfg()
_cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
_cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
_cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")

# Keypoints predictor
_predictor = DefaultPredictor(_cfg)
#%%
start_tick = time.time()
outputs = _predictor(img)
print(f'delay { time.time() - start_tick }')

#%%
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(_cfg.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

display( Image.fromarray(out.get_image()))


# %%
