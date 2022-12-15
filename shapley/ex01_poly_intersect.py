#%%
import shapely
from shapely.geometry import Point, Polygon, LineString, GeometryCollection
import numpy as np

import cv2
from PIL import Image
from IPython.display import display


#%%
img = np.zeros((128,128,3),np.uint8)
pts = np.array([[10,10],[64,10],[64,64],[10,64]], np.int32)
pts2 = np.array([[20,15],[100,35],[90,70],[100,110]], np.int32)

_pts = pts.reshape((-1,1,2))
_pts2 = pts2.reshape((-1,1,2))

print(_pts.shape)
cv2.polylines(img,[_pts],True,(0,255,255))
cv2.polylines(img,[_pts2],True,(0,255,255))

display( Image.fromarray(img) )

#%%
poly1 = Polygon(pts)
poly2 = Polygon(pts2)

#calc intersection
_intersec = poly1.intersection(poly2)

# np.array로 변환
_npInsec = np.asarray(list(zip(*_intersec.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))

cv2.polylines(img,[_npInsec],True,(255,0,0),2)

display( Image.fromarray(img) )

# %%
img = np.zeros((128,128,3),np.uint8)
pts1 = np.array([[10,10],[64,10],[64,64],[10,64]], np.int32)
pts2 = np.array([[16,16],[32,16],[32,32],[16,32]], np.int32)

cv2.polylines(img,[pts1.reshape((-1,1,2))],True,(0,255,255))
cv2.polylines(img,[pts2.reshape((-1,1,2))],True,(0,255,255))    

poly1 = Polygon(pts1)
poly2 = Polygon(pts2)

#calc intersection
_insec = poly1.intersection(poly2)

#conver numpy
_npInsec = np.asarray(list(zip(*_insec.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))

cv2.polylines(img,
    [_npInsec],
    True,(255,0,0),2)

display( Image.fromarray(img) )

# %%
