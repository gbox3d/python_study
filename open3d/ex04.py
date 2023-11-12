import open3d as o3d
import numpy as np
import pygame
from pygame.locals import *

from rs2_device_manager import Rs2DeviceManagers


# Rs2DeviceManagers 초기화 및 시작
dm = Rs2DeviceManagers()
dm.start_device_managers()
_device = dm.get_device_manager(0)
_device.start()


geometry_added = False  # 포인트 클라우드 추가 여부 플래그
pcd = o3d.geometry.PointCloud()
def update_geometry(vis):
    global geometry_added
    
    points_3d, colors = _device.getPointCloud(8)

#     # 포인트 클라우드 데이터 업데이트
    pcd.points = o3d.utility.Vector3dVector(points_3d)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    if not geometry_added:
        vis.add_geometry(pcd)
        geometry_added = True
    else:
        vis.update_geometry(pcd)
    


# Open3D Visualizer 설정
vis = o3d.visualization.Visualizer()
vis.create_window(window_name='Open3D', width=640, height=480)
vis.register_animation_callback(update_geometry)
vis.run()

_device.stop()
vis.destroy_window()

