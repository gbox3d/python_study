#%%
from sympy import Point, Polygon, Line, N
import numpy as np
import cv2
from PIL import Image
from IPython.display import display

img = np.zeros((512,512,3),np.uint8)

# Line parameters
start_point = Point(200, 200)
end_point = Point(300, 300)
line = Line(start_point, end_point)

# Polygon parameters
poly = Polygon((10, 10), (64, 10), (64, 64), (10, 64))
poly2 = Polygon((410, 410), (464, 410), (464, 464), (410, 464))

# Draw the line and polygon
# cv2.line(img, (255, 255), (500, 500), (255, 0, 0), 1)
cv2.line(img, (int(start_point.x), int(start_point.y)), (int(end_point.x), int(end_point.y)), (255, 0, 0), 1)   

cv2.polylines(img, [np.array(poly.args).reshape((-1, 1, 2)).astype(np.int32)], True, (0, 255, 255))
cv2.polylines(img, [np.array(poly2.args).reshape((-1, 1, 2)).astype(np.int32)], True, (0, 255, 255))

# Calculate the intersection
intersec =  poly.intersection(line)
intersec2 =  poly2.intersection(line)

# Draw the intersection points that lie along the direction of the line
for _in in intersec:
    _in_eval = N(_in)
    dx1, dy1 = end_point.x - start_point.x, end_point.y - start_point.y
    dx2, dy2 = _in_eval.x - start_point.x, _in_eval.y - start_point.y
    if dx1 * dx2 + dy1 * dy2 >= 0:  # if the intersection point lies in the direction of the line
        cv2.circle(img, (int(_in_eval.x), int(_in_eval.y)), 3, (255, 0, 0), -1)

for _in in intersec2:
    _in_eval = N(_in)
    dx1, dy1 = end_point.x - start_point.x, end_point.y - start_point.y
    dx2, dy2 = _in_eval.x - start_point.x, _in_eval.y - start_point.y
    if dx1 * dx2 + dy1 * dy2 >= 0:  # if the intersection point lies in the direction of the line
        cv2.circle(img, (int(_in_eval.x), int(_in_eval.y)), 3, (255, 0, 0), -1)

# Show the image
display(Image.fromarray(img))

# %%
