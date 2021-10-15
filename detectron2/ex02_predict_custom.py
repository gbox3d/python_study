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
img = cv2.imread("../../datasets/Microcontroller Segmentation/test/IMG_20181228_102757.jpg")
print(img.shape)
 
#%% instance segmentation
# create config for instance segmentation
cfg_instance_seg = get_cfg()
cfg_instance_seg.merge_from_file('./configs/microcontroller_config.yaml')
cfg_instance_seg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_instance_seg.MODEL.WEIGHTS = './output/model_final.pth'
cfg_instance_seg.MODEL.ROI_HEADS.NUM_CLASSES = 4

# instance segmentation predictor
instance_segmentation_predictor = DefaultPredictor(cfg_instance_seg)

start_tick = time.time()
outputs = instance_segmentation_predictor(img)
# using `Visualizer` to draw the predictions on the image.
v = Visualizer( cv2.cvtColor(img,cv2.COLOR_BGR2RGB), MetadataCatalog.get(cfg_instance_seg.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
print(f'delay { time.time() - start_tick }')
display( Image.fromarray(out.get_image()))

# %%
