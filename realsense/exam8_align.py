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
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

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
display(Image.fromarray(color_image))
# %%
depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
display( Image.fromarray( cv2.cvtColor(depth_colormap,cv2.COLOR_BGR2RGB) ) )


##############################################################-----###########################
# %%

# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()

# depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
# depth_intrinsics = depth_profile.get_intrinsics()
# color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
# # Get the extrinsics (디바이스에서 얻은 extrinsics 사용)
# depth_to_color_extrinsics = depth_profile.get_extrinsics_to(color_profile)

# frames = pipeline.wait_for_frames()
# depth_frame = frames.get_depth_frame()
# color_frame = frames.get_color_frame()

# # Convert images to numpy arrays
# depth_image = np.asanyarray(depth_frame.get_data())
# color_image = np.asanyarray(color_frame.get_data())

# # Project depth data to color image
# depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
# colorized_depth = np.asanyarray(depth_colormap)
# colorized_depth[depth_image == 0] = 0

# #%%
# display(Image.fromarray(colorized_depth))

# #%%
# # 뎁스 이미지에서 컬러 이미지로 좌표계 변환
# # Convert extrinsics object to numpy array
# R = np.array(depth_to_color_extrinsics.rotation).reshape(3, 3)
# T = np.array(depth_to_color_extrinsics.translation)
# extrinsics_matrix = np.column_stack((R, T))
# extrinsics_matrix = np.vstack((extrinsics_matrix, [0, 0, 0, 1]))

# # Slice the 3x3 transformation matrix and convert to np.float32
# extrinsics_matrix = np.float32(extrinsics_matrix[:3, :3])

# colorized_depth = cv2.warpPerspective(colorized_depth, extrinsics_matrix, (color_image.shape[1], color_image.shape[0]))

# display(Image.fromarray(colorized_depth))
# # %%
