#%%
import numpy as np
import cv2

from PIL import Image
from IPython.display import display

#%%
color_image = cv2.imread("color_image.jpg", cv2.IMREAD_COLOR)

display( Image.fromarray( cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB) ) )


# %%
# read depth image

depth_image = np.fromfile("depth_image.raw", dtype=np.uint16)
#reshape 640 480

depth_image = depth_image.reshape(480, 640)

display( Image.fromarray( cv2.cvtColor(cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET),cv2.COLOR_BGR2RGB) ) )

# %%
