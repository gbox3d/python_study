#%%
import torch

#%%
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom


# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

#%%
# Inference
results = model(img)
# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# %%
results.pandas().xyxy[0]

# %%
results.pandas().xyxy[0].to_json(orient="records")

# %%
xyxy_pred = results.xyxy[0]
xyxy_pred.shape
# %%
for *box, conf, cls in reversed(xyxy_pred):
    xmin = int(box[0])
    ymin = int(box[1])
    xmax = int(box[2])
    ymax = int(box[3])
    print(xmin,ymin,xmax,ymax , float(conf), int(cls))
    # print( int(cls))
# %%
