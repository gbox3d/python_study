#%%
import pyrealsense2 as rs
import numpy as np
import open3d as o3d


#%%
# Create a RealSense pipeline
pipeline = rs.pipeline()

# Create a configuration for the pipeline
config = rs.config()

# Enable depth and color streams
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
profile = pipeline.start(config)

# Get the depth sensor and color sensor intrinsics
depth_sensor = profile.get_device().first_depth_sensor()
# depth_intrinsics = depth_sensor.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()

depth_stream = rs.stream.depth
depth_profile = next(p for p in profile.get_streams() if p.stream_type() == depth_stream)
depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsics()


color_intrinsics = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

# Define a function to convert depth image to point cloud
def depth_to_pointcloud(depth_image, intrinsics):
    # Get the image width and height
    width = depth_image.shape[1]
    height = depth_image.shape[0]
    # Create arrays of x and y coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x = x.flatten()
    y = y.flatten()
    # Get the depth values and convert them to meters
    depth = depth_image.flatten() * depth_sensor.get_depth_scale()
    # Convert the x, y, and depth values to 3D coordinates
    x = (x - intrinsics.ppx) / intrinsics.fx * depth
    y = (y - intrinsics.ppy) / intrinsics.fy * depth
    z = depth
    # Create a point cloud object
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(np.vstack((x, y, z)).T)
    return pointcloud

def depth_to_pointcloud_rect(depth_image, intrinsics, x_min, x_max, y_min, y_max):
    # Get the image width and height
    width = depth_image.shape[1]
    height = depth_image.shape[0]
    # Create arrays of x and y coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x = x.flatten()
    y = y.flatten()
    # Get the depth values and convert them to meters
    depth = depth_image.flatten() * depth_sensor.get_depth_scale()
    # Convert the x, y, and depth values to 3D coordinates
    x = (x - intrinsics.ppx) / intrinsics.fx * depth
    y = (y - intrinsics.ppy) / intrinsics.fy * depth
    z = depth
    # Filter the points to only include those within the rectangle
    mask = (x >= x_min) & (x < x_max) & (y >= y_min) & (y < y_max)
    x = x[mask]
    y = y[mask]
    z = z[mask]
    # Create a point cloud object
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(np.vstack((x, y, z)).T)
    return pointcloud


# Define a function to convert color image to RGB array
def color_image_to_array(color_image):
    # Convert the color image to RGB array
    color_array = np.asanyarray(color_image.get_data())
    color_array = color_array[:,:,::-1]
    return color_array
#%%
vis = o3d.visualization.Visualizer()
vis.create_window(visible=False)

# Capture 10 frames
for i in range(10):
    # Wait for a new frame
    frames = pipeline.wait_for_frames()

    # Get the depth and color frames
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # Convert the depth frame to a point cloud
    pointcloud = depth_to_pointcloud(np.asanyarray(depth_frame.get_data()), depth_intrinsics)

    # Convert the color frame to an RGB array
    color_array = color_image_to_array(color_frame)

    # Set the colors of the point cloud
    colors = np.reshape(color_array, (color_intrinsics.height, color_intrinsics.width, 3))
    colors = colors[::2,::2,:] # Downsample the colors to match the point cloud
    colors = np.reshape(colors, (-1, 3))
    pointcloud.colors = o3d.utility.Vector3dVector(colors)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pointcloud])
    
# Stop the pipeline
pipeline.stop()
# vis.destroy_window()

# %%
print(pointcloud.get_min_bound())
print(pointcloud.get_max_bound())
# %%
print(pointcloud.get_center())
print(len(pointcloud.points))
# %%
frames = pipeline.wait_for_frames()

# Get the depth and color frames
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()

x_min, y_min = 100, 100
x_max, y_max = 200, 200
pointcloud_rect = depth_to_pointcloud_rect(np.asanyarray(depth_frame.get_data()), depth_intrinsics, x_min, x_max, y_min, y_max)

# %%
