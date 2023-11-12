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

# z으로 0.1만큼 이동 행렬
transformation = np.array([[1,0,0,0],
                           [0,1,0,0],
                           [0,0,1,0.5],
                           [0,0,0,1]])

#%%
_pcd2 = copy.deepcopy(pcd1).transform(transformation)
o3d.visualization.draw_geometries([pcd1,_pcd2])

#%%
_device.stop()