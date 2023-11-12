#%%
import open3d as o3d
import numpy as np
import copy
# import pygame
# from pygame.locals import *

from rs2_device_manager import Rs2DeviceManagers


# Rs2DeviceManagers 초기화 및 시작
dm = Rs2DeviceManagers()
dm.start_device_managers()
_device = dm.get_device_manager(0)
_device.start()

#%%
pcd1 = o3d.geometry.PointCloud()
points_3d,colors = _device.getPointCloud(8)
pcd1.points = o3d.utility.Vector3dVector(points_3d)
pcd1.colors = o3d.utility.Vector3dVector(colors)

#%%
pcd2 = o3d.geometry.PointCloud()
points_3d,colors = _device.getPointCloud(8)
pcd2.points = o3d.utility.Vector3dVector(points_3d)
pcd2.colors = o3d.utility.Vector3dVector(colors)

#%%
def register_point_clouds(source_cloud, target_cloud):
    # 포인트 클라우드를 Open3D 객체로 변환
    # source_cloud = o3d.geometry.PointCloud()
    # source_cloud.points = o3d.utility.Vector3dVector(source)
    # target_cloud = o3d.geometry.PointCloud()
    # target_cloud.points = o3d.utility.Vector3dVector(target)

    # ICP 등록
    threshold = 0.1  # 최대 거리 임계값 (두 포인트 클라우드 간의 대략적인 거리 차이)
    trans_init = np.identity(4)  # 초기 변환 행렬 (단위 행렬)
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source_cloud, target_cloud, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())

    # 결과 변환 행렬 반환
    return reg_p2p.transformation

transformation = register_point_clouds(pcd1,pcd2)

#%%
# _pcd2 = pcd1.transform(transformation)
_pcd1 = copy.deepcopy(pcd1).transform(transformation)
o3d.visualization.draw_geometries([_pcd1,pcd2])

#%%
_device.stop()