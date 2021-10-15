#!/bin/bash
wget http://images.cocodataset.org/val2017/000000439715.jpg -q -O ../res/input.jpg
wget http://farm5.staticflickr.com/4040/4212024872_c8f721ab0a_z.jpg -q -O ../res/orange.jpg

#download source https://cocodataset.org/#explore

# download datastes
wget https://github.com/TannerGilbert/Detectron2-Train-a-Instance-Segmentation-Model/raw/master/microcontroller_segmentation_data.zip
wget https://github.com/matterport/Mask_RCNN/releases/download/v2.1/balloon_dataset.zip -O ../../datasets
wget https://github.com/Tony607/detectron2_instance_segmentation_demo/releases/download/V0.1/data.zip -q -O ../../datasets/fruts_nuts.zip