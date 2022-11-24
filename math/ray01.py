#%%
import numpy as np
import cv2 as cv
from PIL import Image
from IPython.display import display

def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):

	ndotu = planeNormal.dot(rayDirection)
	if abs(ndotu) < epsilon:
		raise RuntimeError("no intersection or line is within plane")

	w = rayPoint - planePoint
	si = -planeNormal.dot(w) / ndotu
	Psi = w + si * rayDirection + planePoint
	return Psi
#%%
planeNormal = np.array([0, 1, 0])
planePoint = np.array([0, 400, 0]) #Any point on the plane

#Define ray
lwr = np.array([100, 100, 0]) #Ray direction
rwr = np.array([150, 200, 0]) #Ray origin

rayDirection = lwr-rwr

_dist = np.linalg.norm(rayDirection)
print( round(_dist,3))

rayDirection = rayDirection / np.linalg.norm(rayDirection)

# rayDirection = np.array([0, -1, -1])
rayPoint = rwr #Any point along the ray

Psi = LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint)
print ("intersection at", Psi)

#%%
img = np.zeros((480,640,3),np.uint8)
img = cv.line(img,
    tuple(lwr[0:2]),tuple(rwr[0:2]),
    (255,0,0) # BRG color
    ,5)
img = cv.line(img,
    (planePoint[0],planePoint[1]),(planePoint[0]+640,planePoint[1]),
    (255,255,0) # BRG color
    ,5)
img = cv.circle(img,
    tuple(Psi[0:2].astype(np.int)),  #중심정 
    8, #지름  
    (0,0,255), 
    -1 # 칠하기 
)

display( Image.fromarray(img) )

# %%
