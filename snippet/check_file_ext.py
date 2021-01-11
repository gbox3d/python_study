#%%
import os
import sys
import pathlib

print(pathlib.Path.cwd())


img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng']  # acceptable image suffixes
files = ["1.png","test.txt","2.jpg","yolo5s.weight"]

print(files[3].split('.')[-1]) # 확장자 구하기

# 특정 확장자만 골라내기 
images = [x for x in files if x.split('.')[-1].lower() in img_formats]

print(images)
# %%
