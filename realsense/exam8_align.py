#%%
import pyrealsense2 as rs
import numpy as np
import cv2

from PIL import Image
from IPython.display import display
#%%
# RealSense context 생성
context = rs.context()
# 연결된 모든 RealSense 장치의 정보 얻기
devices = context.query_devices()
# 모든 장치의 이름 출력
for dev in devices:
    print(dev.get_info(rs.camera_info.name))
camera_model = devices[0].get_info(rs.camera_info.name)

# %%
pipeline = rs.pipeline()
config = rs.config()
if (camera_model == 'Intel RealSense L515'):
    config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else :
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Aligning Depth to Color
align = rs.align(rs.stream.color)

#start camera
profile = pipeline.start(config)

#%%
#get frames
frames = pipeline.wait_for_frames()
aligned_frames = align.process(frames)
depth_frame = aligned_frames.get_depth_frame()
color_frame = aligned_frames.get_color_frame()

# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())
#%%
display(Image.fromarray( cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB) ))
# %%
depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
display( Image.fromarray( cv2.cvtColor(depth_colormap,cv2.COLOR_BGR2RGB) ) )

