#%%
# First import the library
import pyrealsense2 as rs

#%%
pipeline = rs.pipeline()

# Configure streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

#%%
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()

dist = depth.get_distance(100, 100)

print(dist)

# %%
