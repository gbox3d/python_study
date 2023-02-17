#%%
import pyrealsense2 as rs
import numpy as np
import cv2

from PIL import Image
from IPython.display import display


#%%
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

print("device_product_line: ", device_product_line)
print("found_rgb: ", found_rgb)
print("init ok")
#%%
# Start streaming
pipeline.start(config)
print("start ok")
#%%
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()
print("depth_frame: ", depth_frame.height, depth_frame.width, depth_frame.get_data_size(), depth_frame.get_stride_in_bytes(), depth_frame.get_bytes_per_pixel())
print("get 320,240 pixel: ", depth_frame.get_distance(320,240))
print("data type: ", type(depth_frame.get_data()))

depth_image = np.asanyarray(depth_frame.get_data())
print("depth_image: ", depth_image.shape, depth_image.dtype)

# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())

#%%
display( Image.fromarray( cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB) ) )
cv2.imwrite("color_image.jpg", color_image)

#%% save depth image
depth_image.tofile("depth_image.raw")

# display( Image.fromarray( depth_image ) )
# depth_map = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
# cv2.imwrite("depth_image.jpg", depth_map)
# display( Image.fromarray( depth_map ) )

#%%
print("data type: ", type(depth_image))
print(depth_image.shape)
print(depth_image.dtype)
print(depth_image[240,320])
print("get 320,240 pixel: ", depth_frame.get_distance(320,240))

#%%
# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
display( Image.fromarray( cv2.cvtColor(cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET),cv2.COLOR_BGR2RGB) ) )


# %%
# Stop streaming
pipeline.stop()
print("stop ok")
