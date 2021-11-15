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


# import some common libraries
import numpy as np

import detectron2
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer,GenericMask
from detectron2.data import MetadataCatalog, DatasetCatalog

print(f'detectron : {detectron2.__version__}')
#%% object detection
img = cv2.imread("./bird1.jpg")
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
# predict = outputs["instances"].to("cpu")
print(f'delay { time.time() - start_tick }')

# %% mask pixel count 
pred_masks = outputs["instances"].pred_masks.cpu().numpy()
for mask in pred_masks:
    # mask = mask.cpu().numpy()
    _mask = GenericMask(mask, img.shape[0], img.shape[1])
    np_cnt = np.array(_mask.polygons,dtype=np.int32).reshape((-1, 2))
    out_img = cv2.polylines(_mask.mask, [np_cnt], True, (4), thickness=1)
    display(Image.fromarray(out_img * 63))
    print( f'mask pixel count : {np.count_nonzero(_mask.mask != 0)}' )

# %%
print(outputs["instances"].pred_classes.cpu().numpy().tobytes())
print(outputs["instances"].scores.cpu().numpy().tobytes())
print( np.array([box.cpu().numpy() for box in outputs["instances"].pred_boxes]).tobytes() )

# %%
generic_masks = [GenericMask(x, img.shape[0], img.shape[1]) for x in pred_masks]

#%%
for gen_mask in generic_masks:
    print(np.array(gen_mask.polygons).shape)
    
    # mask = mask.cpu().numpy()

# %%
