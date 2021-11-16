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
img = cv2.imread("../../bird1.jpg")
print(img.shape)
display(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))

#%% instance segmentation
# create config for instance segmentation
cfg_instance_seg = get_cfg()
cfg_instance_seg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg_instance_seg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg_instance_seg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")


# instance segmentation predictor
instance_segmentation_predictor = DefaultPredictor(cfg_instance_seg)
#%%
start_tick = time.time()
outputs = instance_segmentation_predictor(img)
print(f'delay { time.time() - start_tick }')

# %%
pred_masks = outputs["instances"].pred_masks
for mask in pred_masks:
    mask = mask.cpu().numpy()
    # mask = mask.astype(np.uint8)
    display(Image.fromarray(mask))
# %%
