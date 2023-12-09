#%%
import numpy as np
import open3d as o3d

# 3개의 점을 정의합니다.
points = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]])

# 이 점들을 사용하여 3각형 메시를 생성합니다.
triangles = np.array([[0, 1, 2]])
mesh = o3d.geometry.TriangleMesh(
    o3d.utility.Vector3dVector(points),
    o3d.utility.Vector3iVector(triangles),
)

# 메시의 색상을 설정합니다.
colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

# 메시를 원점을 중심으로 180도 회전합니다.
R = mesh.get_rotation_matrix_from_xyz((0, np.pi, 0))
mesh.rotate(R, center=(0,0,0))

#%%
# 메시를 시각화합니다.
o3d.visualization.draw_geometries([mesh])

# %%
