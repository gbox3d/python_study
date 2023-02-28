#%%
import pyrealsense2 as rs

import numpy as np

# 카메라 초기화
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

profile = pipeline.start(config)

# 내부 매개 변수 및 외부 매개 변수 가져오기
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))

color_stream = profile.get_stream(rs.stream.color)
color_profile = rs.video_stream_profile(color_stream)

intrinsics = depth_profile.get_intrinsics()


#%% 수동으로 입력하는 위치와 각도
# 수동으로 직접 생성하는 extrinsics 사용 
x, y, z = 0, 0, 0
angle_degrees = 45

# 각도를 라디안으로 변환
angle_radians = np.deg2rad(angle_degrees)

# 회전 매트릭스 생성
rotation = np.array([
    [1, 0, 0],
    [0, np.cos(angle_radians), -np.sin(angle_radians)],
    [0, np.sin(angle_radians), np.cos(angle_radians)],
])

# 변환 매트릭스 생성
translation = [x, y, z]
extrinsics = rs.extrinsics()
# 1차원리스트로 변환
extrinsics.rotation = rotation.flatten().tolist()

extrinsics.translation = translation

print("Depth Intrinsics: ", intrinsics)
print("Depth to Color Extrinsics: ", extrinsics)


# %%
# 특정 픽셀의 3D 좌표 구하기
x = 320   # 예시: 가운데 픽셀의 x 좌표
y = 240   # 예시: 가운데 픽셀의 y 좌표
depth = pipeline.wait_for_frames().get_depth_frame().get_distance(x, y)

# 2D 이미지 좌표를 3D 좌표계로 변환
point_2d = np.array([x, y])
point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, point_2d, depth)

print("Pixel ({}, {}) maps to point {}".format(x, y, point_3d))

# %%
