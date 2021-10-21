#%%
import torch
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader

from detectron2.config import get_cfg

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

from detectron2.utils.visualizer import Visualizer,ColorMode
from detectron2.engine import DefaultPredictor

import utils

#%% register dataset 
utils.register_Dataset(
        label_names = ['white-king', 'white-queen', 'white-bishop', 'white-knight', 'white-rook', 'white-pawn','black-king','black-queen', 'black-bishop', 'black-knight', 'black-rook', 'black-pawn','bishop'],
        dataset_name='chess'
    )
_meta = MetadataCatalog.get("chess_test") # 메타데이터 추출 
# %%
config_path = './configs/chess/config.yaml'
cfg = get_cfg()
cfg.merge_from_file(config_path)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = './output/model_final.pth'
cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(_meta.thing_classes)
# instance segmentation predictor
predictor = DefaultPredictor(cfg)


#%%
evaluator = COCOEvaluator("chess_test", output_dir="./output")
val_loader = build_detection_test_loader(cfg, "chess_test")

print(inference_on_dataset(predictor.model, val_loader, evaluator))
# another equivalent way to evaluate the model is to use `trainer.test`


# %%
from detectron2.data import DatasetMapper, build_detection_test_loader
data_loader = build_detection_test_loader(
    cfg,
    cfg.DATASETS.TEST[0],
    DatasetMapper(cfg,True)
)
#%%
print(len(data_loader))
# %%
for idx, inputs in enumerate(data_loader):  
    # print(inputs)
    metrics_dict = predictor.model(inputs)
    print(metrics_dict.values)

    # for k, v in metrics_dict.items() :
    #     print(k,isinstance(v, torch.Tensor))
    #     print(v)
        
    
    
    # metrics_dict = {
    #         k: v.detach().cpu().item() if isinstance(v, torch.Tensor) else float(v)
    #         for k, v in metrics_dict.items()
    #     }
    # total_losses_reduced = sum(loss for loss in metrics_dict.values())
    # print(total_losses_reduced)

# %%
