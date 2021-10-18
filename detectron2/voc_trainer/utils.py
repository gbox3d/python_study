#%%
import os
import numpy as np
import json
from detectron2.structures import BoxMode
import itertools
import cv2
import xml.etree.ElementTree as ET


#%%
def loadVocDataset(dataset_path,dataset_name) :

    annotation_path =  os.path.join(dataset_path,dataset_name)
    image_path = os.path.join(dataset_path,dataset_name)

    dataset_dicts = []
    for idx, filename in enumerate(os.listdir(annotation_path)):
        record = {}
        root = ET.parse(os.path.join(annotation_path, filename)).getroot()
        record["file_name"] = os.path.join(image_path, root.find('filename').text)
        
        # record["height"] = 2248
        # record["width"] = 4000
