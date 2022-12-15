#%%
from sympy import Point, Polygon
import cv2

import numpy as np

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

#%% convert to sympy
poly1 = Polygon(*pts)
poly2 = Polygon(*pts2)

#%%

_intersec =  poly1.intersection(poly2)
# print(_intersec)

for _in in _intersec:
    __in = _in.evalf()
    cv2.circle(img, (int(__in.x),int(__in.y)), 3, (255,0,0), -1)

display( Image.fromarray(img) )
    

  
# #%%
# # creating points using Point()
# p1, p2, p3, p4 = map(Point, [(0, 0), (1, 0), (5, 1), (0, 1)])
# p5, p6, p7 = map(Point, [(3, 2), (1, -1), (0, 2)])
  
# # creating polygons using Polygon()
# poly1 = Polygon(p1, p2, p3, p4)
# poly2 = Polygon(p5, p6, p7)
  
# # using intersection()
# _intersec = poly1.intersection(poly2)
  
# #%%
# for _in in _intersec:
#     _in_eval = _in.evalf()
#     print(f'x: {_in_eval.x}, y: {_in_eval.y}')
# # print(isIntersection)
# # %%
# # %%
