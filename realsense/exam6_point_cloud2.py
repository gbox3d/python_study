#%%
import pyrealsense2 as rs
import numpy as np

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

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))

intrinsics = depth_profile.get_intrinsics()

#%%
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

# %%
# 특정 픽셀의 3D 좌표 구하기
x = 320   # 예시: 가운데 픽셀의 x 좌표
y = 240   # 예시: 가운데 픽셀의 y 좌표
depth = pipeline.wait_for_frames().get_depth_frame().get_distance(x, y)

# 2D 이미지 좌표를 3D 좌표계로 변환
# point_2d = np.array([x, y])
point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [x,y], depth)

print("Pixel ({}, {}) maps to point {}".format(x, y, point_3d))

# %%
