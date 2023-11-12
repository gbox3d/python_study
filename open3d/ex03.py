#%%
import open3d as o3d
import numpy as np
import cv2 as cv
import numpy as np

from PIL import Image
from IPython.display import display
import yaml
import os

import time
from struct import *

from rs2_device_manager import Rs2DeviceManagers

#%%
dm = Rs2DeviceManagers()
dm.start_device_managers()
_device = dm.get_device_manager(0)
_device.start()

#%%
def create_meshes_from_gridded_point_cloud(points_3d, grid_size=(3, 3, 3)):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_3d)

    # 포인트 클라우드의 경계 구하기
    min_bound = point_cloud.get_min_bound()
    max_bound = point_cloud.get_max_bound()

    # 그리드 크기 계산
    grid_step = (max_bound - min_bound) / np.array(grid_size)

    # 각 그리드에 대한 메쉬 생성
    meshes = []
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            for k in range(grid_size[2]):
                # 그리드 경계 설정
                min_corner = min_bound + grid_step * np.array([i, j, k])
                max_corner = min_bound + grid_step * np.array([i + 1, j + 1, k + 1])

                # 해당 그리드 내 포인트 필터링
                grid_points = np.asarray(point_cloud.points)
                in_grid_mask = np.all((grid_points >= min_corner) & (grid_points < max_corner), axis=1)
                grid_point_cloud = grid_points[in_grid_mask]

                # 해당 그리드의 포인트 클라우드로 메쉬 생성
                if len(grid_point_cloud) >= 4:
                    grid_point_cloud_o3d = o3d.geometry.PointCloud()
                    grid_point_cloud_o3d.points = o3d.utility.Vector3dVector(grid_point_cloud)
                    try :
                        mesh = grid_point_cloud_o3d.compute_convex_hull()[0]  # 예시로 Convex Hull 사용
                        meshes.append(mesh)                        
                    except RuntimeError as e:
                        print(f'계산 오류 발생 {e}')
                        pass
                else :
                    print(f'포인트 수 부족 {len(grid_point_cloud)}')
                    

    return meshes

#%%
_starttime = time.time()
points_3d,color_image = _device.getPointCloud(8)
#시간 지연 표시
print(f'delay : {time.time()-_starttime}')
# 그리드 분할 및 메쉬 생성
meshes = create_meshes_from_gridded_point_cloud(points_3d, grid_size=(3, 3, 3))
print(f'len of meshes: {len(meshes)}')
_device.stop()

#%%
print(type(meshes[0]))

#%%
vertices = np.asarray(meshes[0].vertices)
print(vertices.shape)
triangles = np.asarray(meshes[0].triangles)
print(triangles.shape)

# %%
print(vertices)

# %%
