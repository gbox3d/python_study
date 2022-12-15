#%%
import shapely
from shapely.geometry import Point, Polygon, LineString, GeometryCollection
import numpy as np

import cv2
from PIL import Image
from IPython.display import display

#%%
output_img = np.zeros((128,128,3),np.uint8)
poly1 = Polygon( [[10,10],[64,10],[64,64],[10,64]] )

#np.array로 변환
np_poly = np.asarray(list(zip(*poly1.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))
print(np_poly)

cv2.polylines(output_img,[np_poly],True,(0,255,0))
display( Image.fromarray(output_img) )
print('area' , poly1.area)


# %% 면적 
output_img = np.zeros((128,128,3),np.uint8)
poly1 = Polygon( [[15,15],[64,10],[64,64],[10,64]] )

#np.array로 변환
np_poly = np.asarray(list(zip(*poly1.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))
print(np_poly)

cv2.polylines(output_img,[np_poly],True,(0,255,0))
display( Image.fromarray(output_img) )
print('area' , poly1.area)
# print('bounds' , poly1.bounds)

# %% 중심점
np_center = np.asarray(list(zip(*poly1.centroid.coords.xy)), dtype=np.int32)
# print(np_center.squeeze())
cv2.circle(output_img, tuple(np_center.squeeze()), 5, (255,255,0), -1)
display( Image.fromarray(output_img) )
print('centroid' , poly1.centroid)


# %% 바운드 
_bound = poly1.bounds
#numpy array로 변환
np_bound = np.asarray(_bound,dtype=np.int32)
np_bound = np_bound.reshape(-1,2)

print(np_bound)
cv2.rectangle(output_img, tuple(np_bound[0]),tuple(np_bound[1]), (255,0,0), 1)
display( Image.fromarray(output_img) )

