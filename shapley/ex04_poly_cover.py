#%%
import shapely
from shapely.geometry import Point, Polygon, LineString, GeometryCollection
import numpy as np

import cv2
from PIL import Image
from IPython.display import display


#%%
img = np.zeros((128,128,3),np.uint8)
poly1 = Polygon([[10,10],[64,10],[64,64],[10,64]])
poly2 = Polygon([[16,16],[32,16],[32,32],[16,32]])
poly3 = Polygon([[48,32],[72,32],[72,72],[32,72]])

cv2.polylines(img,[np.array(list(zip(*poly1.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))],True,(0,255,0))
cv2.polylines(img,[np.array(list(zip(*poly2.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))],True,(255,255,0))
cv2.polylines(img,[np.array(list(zip(*poly3.exterior.coords.xy)), dtype=np.int32).reshape((-1,1,2))],True,(255,255,255))

display( Image.fromarray(img) )
# %%

print('poly1 covers polys :', poly1.covers(poly2))
print('poly2 covered by poly1 :', poly2.covered_by(poly1))

print('poly1 cover by poly3 :',poly1.covers(poly3))
# %%
