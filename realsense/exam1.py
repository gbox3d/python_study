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

# while True:
    # This call waits until a new coherent set of frames is available on a device
    # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()
    
#%%

dist = depth.get_distance(100, 100)

print(dist)
