#%%
import os
import random
from IPython.core.display import display
import matplotlib.pyplot as plt
import PIL.Image as Image
from IPython.display import display

import cv2
import numpy as np
from detectron2.utils.logger import setup_logger
import detectron2
import torch
import torchvision

# check pytorch installation:
print(torch.__version__, torch.cuda.is_available())
# please manually install torch 1.9 if Colab changes its default version
# assert torch.__version__.startswith("1.9")

from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

from detectron2.utils.visualizer import Visualizer,ColorMode
# from detectron2.engine import DefaultPredictor


#%%
register_coco_instances("microcontroller_test",{},
"../../datasets/Microcontroller Segmentation/test.json",
"../../datasets/Microcontroller Segmentation/test"
)

#%%
dataset_dicts = DatasetCatalog.get("microcontroller_test")
print(dataset_dicts[0])
ds_item = dataset_dicts[0]
# print(ds_item["file_name"])

im = cv2.imread(ds_item["file_name"])
display( Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)))


# %%
_meta = MetadataCatalog.get("microcontroller_test")
_meta.thing_colors=[(255,0,0),(0,255,0),(0,0,255),(255,255,0)]
# print(_meta)
print( f'type : {_meta.evaluator_type}' )
print(f'image root : {_meta.image_root}')
print(f'json file path : {_meta.json_file}')
print(f'class list :  {_meta.thing_classes}')
print(f'name : {_meta.name}')

# %%
_d = dataset_dicts[0]
img = cv2.imread(_d["file_name"])
visualizer = Visualizer(img[:, :, ::-1], 
    metadata=_meta, 
    instance_mode=ColorMode.SEGMENTATION, # thing_colors로 지정해준 값을 사용하기 
    scale=1.0)
out = visualizer.draw_dataset_dict(_d) # 데이터셋 그리기 
display( Image.fromarray(out.get_image()))

# %% 저장하기 
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
_,_encodee_img = cv2.imencode('.jpg',cv2.cvtColor(out.get_image(),cv2.COLOR_BGR2RGB),encode_param)

with open('./out.jpg','wb') as fd :
    fd.write( _encodee_img )



# %% 직접 로딩하기
import json

_dataset_dicts = []
json_file = os.path.join("../../datasets/fruts_nuts", "trainval.json")

with open(json_file) as f:
    imgs_anns = json.load(f)

for img_index,_imginfo in enumerate(imgs_anns['images']) :
    record = {}
    file_name = _imginfo['file_name']
    image_id = _imginfo['id']
    print(file_name)




# %%
