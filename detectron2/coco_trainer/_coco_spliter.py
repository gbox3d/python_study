#%%
import os
import random
import cv2
import numpy as np
# from numpy.lib.function_base import append
import torch
import torchvision
import json
import requests
# import detectron2
from detectron2.structures import BoxMode

#%%
def _saveData(image_dir,save_name,_dataObj,_img_set):
    __dataObj = _dataObj.copy()
    __dataObj['images'] = _img_set

    print(f'{save_name} 저장 시작')
    
    for img_index,_imginfo in enumerate(_img_set) :
        file_name = _imginfo['file_name']
        file_path = os.path.join(image_dir, file_name)
        if 'width' not in _imginfo.keys() or 'height' not in _imginfo.keys():
            img = cv2.imread(file_path)
            _imginfo['width'] = img.shape[1]
            _imginfo['height'] = img.shape[0]
        print(f'{ int(img_index/len(_img_set) * 100) } %',end='\r')
        

    _metaData = list({v['id']:v for v in __dataObj['meta']}.values())
    __dataObj['annotations'] = [ _anno for _anno in _dataObj['annotations'] if _anno['image_id'] in [_img['id'] for _img in _img_set] ]
    __dataObj['meta'] = [ _meta for _meta in _metaData if _meta['id'] in [_img['meta_id'] for _img in _img_set] ]

    for anno in __dataObj['annotations']:
        if anno['bbox']  is None:
            _poly = np.array(anno['segmentation'],dtype=np.int32).flatten()
            np_cnt = _poly.reshape(-1,2)
            x,y,w,h = cv2.boundingRect(np_cnt)
            anno['bbox'] = [x,y,w,h]
        
        if anno['segmentation'] is not None:
            if type(anno['segmentation'][0]) != list :
                anno['segmentation'] = [anno['segmentation']]
        if anno['iscrowd'] == 'Y':
            anno['iscrowd'] = 0



    #save json
    #../../../../datasets/mushroom_data/yangsongyi/_label/train.json
    with open(save_name, 'w') as f:
        anno_num = len(__dataObj["annotations"])
        print(f'{save_name} saved annotaion {anno_num} / img {len(_img_set)}')
        json.dump(__dataObj, f)


def split_CocoDataSetAnnotaion(image_dir, json_file,train_ratio=0.8,test_ratio=0.1,val_ratio=0.1,output_path='output'): 
    with open(json_file) as f:
        _dataObj = json.load(f)
        total_anno = len(_dataObj['images'])
        random.shuffle(_dataObj['images'])

        start_index = 0
        offset = int(total_anno*train_ratio)
        _saveData(image_dir, os.path.join(output_path,'train.json') ,_dataObj,_dataObj['images'][:offset])

        # test set 만들기 
        start_index += offset
        offset = int(total_anno*test_ratio)
        _saveData(image_dir,os.path.join(output_path,'test.json'),_dataObj,_dataObj['images'][start_index: (start_index+offset)])


        # validation set 만들기 
        start_index += offset
        if 1 > train_ratio + test_ratio and val_ratio == 0:
            _saveData(image_dir,os.path.join(output_path,'valid.json'),_dataObj,_dataObj['images'][start_index:])
        elif val_ratio > 0:
            offset = int(total_anno*val_ratio) 
            _saveData(image_dir,os.path.join(output_path,'valid.json'),_dataObj,_dataObj['images'][start_index: (start_index + offset)])
        else:
            print('skip validation set')
            
# %% args parsing 
import argparse
parser = argparse.ArgumentParser(description="coco dataset spliter")
parser.add_argument('--output-path', type=str, 
    default='./output',
    help='help : output path')
parser.add_argument('--json-path', type=str, 
    # default='./out',
    help='help : json path')
parser.add_argument('--img-path', type=str, 
    # default='./out',
    help='help : image path')
parser.add_argument('--test-mode', type=bool,
    default=False)
parser.add_argument('--train-ratio', type=float,default=0.8)
parser.add_argument('--test-ratio', type=float,default=0.1)
parser.add_argument('--val-ratio', type=float,default=0)

# json_file = '../../../../datasets/mushroom_data/yangsongyi/_label/data.json'
# image_dir = '../../../../datasets/mushroom_data/yangsongyi/_image/'

_args = parser.parse_args()

image_path = _args.img_path
json_file = _args.json_path
output_path = _args.output_path
train_ratio = _args.train_ratio
test_ratio = _args.test_ratio
val_ratio = _args.val_ratio


#%%
if _args.test_mode:

    json_file = '../../../../datasets/mushroom_data/yangsongyi/_label/data.json'
    image_dir = '../../../../datasets/mushroom_data/yangsongyi/_image/'

    def test_split_CocoDataSetAnnotaion(image_dir, json_file,train_ratio=0.1,test_ratio=0.1,output_path='output'): 
        with open(json_file) as f:
            _dataObj = json.load(f)
            total_anno = len(_dataObj['images'])
            # random.shuffle(_dataObj['images'])

            _saveData(image_dir, os.path.join(output_path,'train.json') ,_dataObj,_dataObj['images'][0:5])
    test_split_CocoDataSetAnnotaion(image_dir,json_file,)
else :
    split_CocoDataSetAnnotaion(image_dir=image_path,json_file = json_file,output_path=output_path,train_ratio=train_ratio,test_ratio=test_ratio,val_ratio=val_ratio)
# # %%
# json_file = '../../../../datasets/mushroom_data/yangsongyi/_label/data.json'
# image_path = '../../../../datasets/mushroom_data/yangsongyi/_image/'
# split_CocoDataSetAnnotaion(image_dir=image_path,json_file = json_file,output_path='./output',train_ratio=0.01,test_ratio=0.01,val_ratio=0.001)

# %%
