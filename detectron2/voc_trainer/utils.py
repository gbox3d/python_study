#%%
import os
from posixpath import dirname
import logging
import numpy as np
import tempfile
import xml.etree.ElementTree as ET
from collections import OrderedDict, defaultdict
from functools import lru_cache
import torch
import cv2
import time
import datetime

from detectron2.evaluation import evaluator,DatasetEvaluator
from detectron2.structures import BoxMode
from detectron2.data import MetadataCatalog,DatasetCatalog
from detectron2.utils import comm
from detectron2.utils.file_io import PathManager

from detectron2.engine.hooks import HookBase
from detectron2.utils.logger import log_every_n_seconds
from detectron2.data import DatasetMapper, build_detection_test_loader
# import detectron2.utils.comm as comm


#%%
def loadVocDataset(dataset_path,dataset_name,sets_name,classes) :

    annotation_path =  os.path.join(dataset_path,dataset_name,sets_name)
    image_path = annotation_path

    dataset_dicts = []
    for idx, filename in enumerate(os.listdir(annotation_path)):
        
        # print(filename)
        _filename, file_extension = os.path.splitext(filename)
        if file_extension.lower() == '.xml' :
            record = {}
            root = ET.parse(os.path.join(annotation_path, filename)).getroot()
            record["file_name"] = os.path.join(image_path, root.find('filename').text)
            _img = cv2.imread(
                record["file_name"]
                )
            record["height"] = _img.shape[1]
            record["width"] = _img.shape[0]
            record["image_id"] = idx
            objs = []

            for member in root.findall('object'):
                # print(member[4])
                _label = member.find('name').text
                # print(_label)
                _bbox = member.find('bndbox')
                xmin =  float(_bbox.find('xmin').text)
                ymin =  float(_bbox.find('ymin').text)
                xmax =  float(_bbox.find('xmax').text)
                ymax =  float(_bbox.find('ymax').text)

                # for _obj in _bbox :
                    
                obj = {
                    'bbox': [xmin,ymin,xmax,ymax],
                    'bbox_mode': BoxMode.XYXY_ABS,
                    'category_id': classes.index(_label),
                    "iscrowd": 0
                }
                objs.append(obj)
            record["annotations"] = objs
            dataset_dicts.append(record)

    # print(dataset_dicts)
    return dataset_dicts

def register_Dataset(label_names,dataset_name) :
    for d in ['train','valid','test'] :
        # label_names = ['white-king', 'white-queen', 'white-bishop', 'white-knight', 'white-rook', 'white-pawn','black-king','black-queen', 'black-bishop', 'black-knight', 'black-rook', 'black-pawn']
        DatasetCatalog.register(f"{dataset_name}_{d}" , 
                lambda d=d: loadVocDataset(
                        dataset_path='../../../../datasets',
                        dataset_name=dataset_name,
                        sets_name=d,
                        classes=label_names
                    )
                )
                # pascal_voc, sem_seg,coco
        MetadataCatalog.get(f"{dataset_name}_{d}").set(
            thing_classes=label_names,
            evaluator_type='coco',
            dirname=f'../../../../datasets/{dataset_name}'
            )
#%%
# from detectron2.evaluation import DatasetEvaluator

class DummyEvaluator(DatasetEvaluator):
    """
    Evaluate Pascal VOC style AP for Pascal VOC dataset.
    It contains a synchronization, therefore has to be called from all ranks.

    Note that the concept of AP can be implemented in different ways and may not
    produce identical results. This class mimics the implementation of the official
    Pascal VOC Matlab API, and should produce similar but not identical results to the
    official API.
    """

    def __init__(self, dataset_name):
        """
        Args:
            dataset_name (str): name of the dataset, e.g., "voc_2007_test"
        """
        self._dataset_name = dataset_name
        self.meta = MetadataCatalog.get(dataset_name)

    def reset(self):
        self._predictions = defaultdict(list)  # class name -> list of prediction strings

    def process(self, inputs, outputs):
        # print(input)
        # print(len(outputs))
        pass

    def evaluate(self):
        """
        Returns:
            dict: has a key "segm", whose value is a dict of "AP", "AP50", and "AP75".
        """
        pass
class LossEvalHook(HookBase):
    def __init__(self, eval_period, model, data_loader):
        self._model = model
        self._period = eval_period
        self._data_loader = data_loader
    
    def _do_loss_eval(self):
        # Copying inference_on_dataset from evaluator.py
        total = len(self._data_loader)
        num_warmup = min(5, total - 1)
            
        start_time = time.perf_counter()
        total_compute_time = 0
        losses = []
        for idx, inputs in enumerate(self._data_loader):            
            if idx == num_warmup:
                start_time = time.perf_counter()
                total_compute_time = 0
            start_compute_time = time.perf_counter()
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            total_compute_time += time.perf_counter() - start_compute_time
            iters_after_start = idx + 1 - num_warmup * int(idx >= num_warmup)
            seconds_per_img = total_compute_time / iters_after_start
            if idx >= num_warmup * 2 or seconds_per_img > 5:
                total_seconds_per_img = (time.perf_counter() - start_time) / iters_after_start
                eta = datetime.timedelta(seconds=int(total_seconds_per_img * (total - idx - 1)))
                log_every_n_seconds(
                    logging.INFO,
                    "Loss on Validation  done {}/{}. {:.4f} s / img. ETA={}".format(
                        idx + 1, total, seconds_per_img, str(eta)
                    ),
                    n=5,
                )
            loss_batch = self._get_loss(inputs)
            losses.append(loss_batch)
        mean_loss = np.mean(losses)
        self.trainer.storage.put_scalar('validation_loss',mean_loss)
        comm.synchronize()

        # print(losses)
        return losses
            
    def _get_loss(self, data):
        # How loss is calculated on train_loop 
        metrics_dict = self._model(data)
        metrics_dict = {
            k: v.detach().cpu().item() if isinstance(v, torch.Tensor) else float(v)
            for k, v in metrics_dict.items()
        }
        total_losses_reduced = sum(loss for loss in metrics_dict.values())
        # print( total_losses_reduced)
        return total_losses_reduced
        
        
    def after_step(self):
        # self._do_loss_eval()
        next_iter = self.trainer.iter + 1
        # print(next_iter,self.trainer.max_iter,self._period)
        is_final = next_iter == self.trainer.max_iter
        if is_final or (self._period > 0 and self.trainer.iter % self._period == 0 and self.trainer.iter > 0):
            print(f'compute vaild loss at {self.trainer.iter}')
            self._do_loss_eval()
        # self.trainer.storage.put_scalars(timetest=12)




#%%
if __name__ == "__main__" :
    _ds = loadVocDataset(
        dataset_path='../../../../datasets',
        dataset_name='chess',
        sets_name='test',
        classes=['white-king', 'white-queen', 'white-bishop', 'white-knight', 'white-rook', 'white-pawn','black-king','black-queen', 'black-bishop', 'black-knight', 'black-rook', 'black-pawn']
    )
    print(_ds)
# %%
