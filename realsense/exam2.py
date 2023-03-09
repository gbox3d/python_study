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
profile = pipeline.start(config)
print("start ok")

#%%
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))

intrinsics = depth_profile.get_intrinsics()

# Get the extrinsics (디바이스에서 얻은 extrinsics 사용)
depth_to_color_extrinsics = depth_profile.get_extrinsics_to(color_profile)

if "i" in camera_model:
    # imu가 포함된 모델
    print("IMU is included in this model.")
    extrinsics = profile.get_device().first_pose_sensor().get_extrinsics_to(profile.get_stream(rs.stream.depth))
else:
    # imu가 없는 모델
    print("IMU is not included in this model.")
    extrinsics = profile.get_stream(rs.stream.depth).get_extrinsics_to(profile.get_stream(rs.stream.color))


print("Depth Intrinsics: ", depth_intrinsics)
print("Depth to Color Extrinsics: ", depth_to_color_extrinsics)
print("Extrinsics: ", extrinsics)


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
print(depth_image.shape)
print(depth_image[100,100] , depth_frame.get_distance(100,100) )

#%%
display( Image.fromarray( cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB) ) )
# %%
display( Image.fromarray( cv2.cvtColor(depth_colormap,cv2.COLOR_BGR2RGB) ) )
# %%

display( Image.fromarray( cv2.cvtColor(images,cv2.COLOR_BGR2RGB) ) )
# %%

#3d point cloud
# 특정 픽셀의 3D 좌표 구하기
x = 320   # 예시: 가운데 픽셀의 x 좌표
y = 240   # 예시: 가운데 픽셀의 y 좌표
depth = pipeline.wait_for_frames().get_depth_frame().get_distance(x, y)

# 2D 이미지 좌표를 3D 좌표계로 변환
point_2d = np.array([x, y])
point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, point_2d, depth)

print("Pixel ({}, {}) maps to point {}".format(x, y, point_3d))



#%%
# Stop streaming
pipeline.stop()

