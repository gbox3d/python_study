#%%
import pyrealsense2 as rs
import numpy as np
import cv2

from PIL import Image
from IPython.display import display

#%%
print(f'cv version: {cv2.__version__}')
# print(f'realsense version: {rs.get_version()}')

#%%
# RealSense context 생성
context = rs.context()

# 연결된 모든 RealSense 장치의 정보 얻기
devices = context.query_devices()

# 장치가 없는 경우 예외 처리
if len(devices) == 0:
    print("No RealSense devices were detected.")
else:
    # 모든 장치의 이름 출력
    for dev in devices:
        print(dev.get_info(rs.camera_info.name))
    camera_model = devices[0].get_info(rs.camera_info.name)
    camera_name = camera_model.split(' ')[-1]
    print("camera_model: ", camera_name)

#%%
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
print("device_product_line: ", device_product_line)

#%%
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
    if camera_name == 'L515':
        print("L515 depth sensor is set to 1024x768 resolution")
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

print("device_product_line: ", device_product_line)
print("found_rgb: ", found_rgb)
print("init ok")
#%%
# Start streaming
profile = pipeline.start(config)
print("start ok")


#%%
frames = pipeline.wait_for_frames() # Wait for a coherent pair of frames: depth and color
depth_frame = frames.get_depth_frame() # Get depth frame
color_frame = frames.get_color_frame() # Get color frame

# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())

# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

depth_colormap_dim = depth_colormap.shape
color_colormap_dim = color_image.shape

# If depth and color resolutions are different, resize color image to match depth image for display
if depth_colormap_dim != color_colormap_dim:
    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
    images = np.hstack((resized_color_image, depth_colormap))
else:
    images = np.hstack((color_image, depth_colormap))

#%%
display( Image.fromarray( cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB) ) )
# %%
display( Image.fromarray( cv2.cvtColor(depth_colormap,cv2.COLOR_BGR2RGB) ) )
# %%
display( Image.fromarray( cv2.cvtColor(images,cv2.COLOR_BGR2RGB) ) )
#%%
# Stop streaming
pipeline.stop()


# %%
