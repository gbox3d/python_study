import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from struct import *

class Rs2DeviceManager:
    def __init__(self, device):
        
        print("Serial Number: ", device.get_info(rs.camera_info.serial_number))
        print("Firmware Version: ", device.get_info(rs.camera_info.firmware_version))
        print("Physical Port: ", device.get_info(rs.camera_info.physical_port))
        print("Product ID: ", device.get_info(rs.camera_info.product_id))
        print("Product Line: ", device.get_info(rs.camera_info.product_line))
        
        self.device = device # rs2 device
        self.pipeline = rs.pipeline() # create a pipeline
        self.profile = None
        self.align = rs.align(rs.stream.color)
        self.cameraName = device.get_info(rs.camera_info.name).split(' ')[-1]
        
        print("Camera Name: ", self.cameraName)

        self.config = rs.config()
        self.config.enable_device(self.device.get_info(rs.camera_info.serial_number))

        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        if device_product_line == 'L500':
            self.config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
            self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        elif device_product_line == 'D400':
            if self.cameraName == 'D455':
                self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
                self.config.enable_stream(rs.stream.color, 1280, 800, rs.format.bgr8, 30)
            else :
                self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
                self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        print("----------------------------------------")

    def start(self):        
        if self.profile is None:
            self.profile = self.pipeline.start(self.config)
            print(f"camera id : { self.device.get_info(rs.camera_info.serial_number) } started ")
            stream_profile = self.profile.get_stream(rs.stream.color)
            # Extract camera resolution
            self.camera_resolution = (
                stream_profile.as_video_stream_profile().width(), 
                stream_profile.as_video_stream_profile().height())
            
            print("camera_resolution: ", self.camera_resolution)
            
        else:
            print(f"camera id : { self.device.get_info(rs.camera_info.serial_number) } already started ")        

    def stop(self):
        if self.profile is not None:
            self.pipeline.stop()            
            print(f"camera id : { self.device.get_info(rs.camera_info.serial_number) } stopped ")
            self.profile = None
        else:
            print(f"camera id : { self.device.get_info(rs.camera_info.serial_number) } already stopped ")
            
    def get_color_frame(self):
        frames = self.pipeline.wait_for_frames()        
        color_frame = frames.get_color_frame()
        if not color_frame:
            raise RuntimeError("Could not get color frame")
        return color_frame

    def get_depth_frame(self):
        # Align the depth frame to color frame
        frames = self.align.process(self.pipeline.wait_for_frames())
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            raise RuntimeError("Could not get depth frame")
        
        return depth_frame
    
    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        
        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)
        
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        if not aligned_depth_frame or not color_frame:
            raise RuntimeError("Could not get aligned frames")        
        return aligned_depth_frame, color_frame
    
    def getCameraInfo(self):                   
        # Check if the profile is active
        if self.profile:
            # Use the active profile
            stream_profile = self.profile.get_stream(rs.stream.color)
        else:
            # Start the pipeline to get stream profile and stop it afterwards
            self.start()
            stream_profile = self.pipeline.get_active_profile().get_stream(rs.stream.color)
            self.stop()
        
        # Extract camera resolution
        camera_resolution = (stream_profile.as_video_stream_profile().width(), 
                            stream_profile.as_video_stream_profile().height())
        
        return (
            self.device.get_info(rs.camera_info.serial_number),
            self.device.get_info(rs.camera_info.firmware_version),
            self.device.get_info(rs.camera_info.physical_port),
            self.device.get_info(rs.camera_info.product_id),
            self.device.get_info(rs.camera_info.product_line),
            camera_resolution
        )
    def isReady(self):
        if self.profile is None:
            return False
        else:
            return True
    def get_3d_coordinates(self, x, y):
        """
        Get the 3D coordinates of a specific pixel.
        
        Parameters:
        - x: The x-coordinate of the pixel.
        - y: The y-coordinate of the pixel.
        
        Returns:
        - A tuple representing the 3D coordinates of the pixel.
        """
        # Get the depth frame
        depth_frame = self.get_depth_frame()
        
        # Get the depth value at the specified pixel
        depth = depth_frame.get_distance(x, y)
        
        # Get the intrinsics of the depth frame(카메라 랜즈와 이미지센서의 특성을 나타내는 값들 가져오기)
        intrinsics = rs.video_stream_profile(depth_frame.profile).get_intrinsics()
        
        # Convert the 2D pixel to 3D point
        point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
        
        # flip y-axis
        # point_3d = (point_3d[0], -point_3d[1], point_3d[2])
        
        return point_3d
    def get_3d_coordinates_area(self, x, y, w, h):
        """
        Get the 3D coordinates of a specific area.
        
        Parameters:
        - x: The x-coordinate of the starting pixel.
        - y: The y-coordinate of the starting pixel.
        - w: The width of the area.
        - h: The height of the area.
        
        Returns:
        - A list of tuples representing the 3D coordinates of the pixels in the area.
        """
        # Get the depth frame
        depth_frame = self.get_depth_frame()
        
        # Get the intrinsics of the depth frame
        intrinsics = rs.video_stream_profile(depth_frame.profile).get_intrinsics()
        
        coordinates_list = []
        
        for i in range(x, x + w):
            for j in range(y, y + h):
                # Get the depth value at the current pixel
                depth = depth_frame.get_distance(i, j)
                
                # Convert the 2D pixel to 3D point
                point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [i, j], depth)
                
                coordinates_list.append(point_3d)
        
        return coordinates_list
    def get_3d_coordinates_area_downsampled(self, x, y, w, h, downsample_factor=2):
        """
        Get the 3D coordinates of a specific area with downsampled depth data.
        
        Parameters:
        - x, y: The top-left corner of the area.
        - w, h: The width and height of the area.
        - downsample_factor: The factor by which to downsample the depth data.
        
        Returns:
        - A list of 3D coordinates for the specified area.
        """
        # Apply the decimation filter to downsample the depth data
        decimation = rs.decimation_filter()
        decimation.set_option(rs.option.filter_magnitude, downsample_factor)
        
        # Get the depth frame and apply the decimation filter
        depth_frame = self.get_depth_frame()
        # depth_frame_downsampled = decimation.process(depth_frame)
        depth_frame_downsampled = rs.depth_frame(decimation.process(depth_frame))

        
        # if depth_frame_downsampled.is_depth_frame():
        #     depth = depth_frame_downsampled.get_distance(i, j)
        # else:
        #     raise ValueError("The frame is not a depth frame.")
        
        # Calculate the new area dimensions after downsampling
        x_downsampled = int(x / downsample_factor)
        y_downsampled = int(y / downsample_factor)
        w_downsampled = int(w / downsample_factor)
        h_downsampled = int(h / downsample_factor)
        
        # Get the intrinsics of the downsampled depth frame
        intrinsics = rs.video_stream_profile(depth_frame_downsampled.profile).get_intrinsics()
        
        # Extract the 3D coordinates for the specified area
        points_3d = []
        for i in range(x_downsampled, x_downsampled + w_downsampled):
            for j in range(y_downsampled, y_downsampled + h_downsampled):
                depth = depth_frame_downsampled.get_distance(i, j)
                point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [i, j], depth)
                points_3d.append(point_3d)
        
        return x_downsampled,y_downsampled,w_downsampled,h_downsampled, points_3d
    def getPointCloud(self,downsample_factor=2):
        w_downsampled = int( self.camera_resolution[0] / downsample_factor)
        h_downsampled = int( self.camera_resolution[1] / downsample_factor)
        
        decimation = rs.decimation_filter()
        decimation.set_option(rs.option.filter_magnitude, downsample_factor)
        
        # Get the depth frame and apply the decimation filter
        depth_frame,color_frame = self.get_frames()
        depth_frame_downsampled = rs.depth_frame(decimation.process(depth_frame))
        
        # Get the intrinsics of the downsampled depth frame
        intrinsics = rs.video_stream_profile(depth_frame_downsampled.profile).get_intrinsics()
        
        # Initialize numpy arrays for efficiency
        points_3d = np.empty((h_downsampled * w_downsampled, 3))
        color_image = np.asanyarray(color_frame.get_data())
        colors = np.empty((h_downsampled * w_downsampled, 3))

        index = 0
        for i in range(w_downsampled):
            for j in range(h_downsampled):
                depth = depth_frame_downsampled.get_distance(i, j)
                point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [i, j], depth)
                points_3d[index] = point_3d
                _bgr = color_image[j * downsample_factor, i * downsample_factor]/255
                colors[index] = [_bgr[2],_bgr[1],_bgr[0]]
                index += 1
        return points_3d,colors
    
    
    def getPointCloud2Pack(self,downsample_factor=2):
        
        w_downsampled = int( self.camera_resolution[0] / downsample_factor)
        h_downsampled = int( self.camera_resolution[1] / downsample_factor)
        
        decimation = rs.decimation_filter()
        decimation.set_option(rs.option.filter_magnitude, downsample_factor)
        
        # Get the depth frame and apply the decimation filter
        depth_frame,color_frame = self.get_frames()
        depth_frame_downsampled = rs.depth_frame(decimation.process(depth_frame))
        
        # Get the intrinsics of the downsampled depth frame
        intrinsics = rs.video_stream_profile(depth_frame_downsampled.profile).get_intrinsics()
        
        # Initialize numpy arrays for efficiency
        # points_3d = np.empty((h_downsampled * w_downsampled, 3))
        # colors = np.empty((h_downsampled * w_downsampled, 3))
        
        # index = 0
        _byteBuffer = b''
        np_color_image = np.asanyarray(color_frame.get_data())
        # color_image = cv.resize(np_color_image, (w_downsampled, h_downsampled))
        # np_depth_image = np.asanyarray(depth_frame_downsampled.get_data())/1000.0
        
        _color_data = color_frame.get_data()
        # index = 0
        for i in range(w_downsampled):
            for j in range(h_downsampled):
                depth = depth_frame_downsampled.get_distance(i, j)
                point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [i, j], depth)
                _byteBuffer += pack('<fff', *point_3d) # point
                
                # 다운샘플링 비율에 따라 컬러 이미지에서 픽셀 선택
                color = np_color_image[j * downsample_factor, i * downsample_factor]
                # color = color_frame.get_data()[j * downsample_factor, i * downsample_factor]
                _byteBuffer += pack('<BBB', color[2], color[1], color[0])
        _byteBuffer = pack('<LLL', len(_byteBuffer),w_downsampled,h_downsampled) + _byteBuffer
        
        return _byteBuffer
    
        
class Rs2DeviceManagers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Rs2DeviceManagers, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.device_managers = []
        self.init_device_managers()

    def init_device_managers(self):
        context = rs.context()
        devices = context.query_devices() # get a list of devices
    
        if devices.size == 0:
            print("No RealSense devices were found!")
            exit(0)
        else:
            self.device_managers = [Rs2DeviceManager(device) for device in devices]  
    # def start_device_manager(self,index): 
    #     device = self.device_managers[index]
    #     device.start()    
    # def stop_device_manager(self,index):
    #     device = self.device_managers[index]
    #     device.stop()
    def get_device_manager(self,index):
        if index >= len(self.device_managers):
            return None
        return self.device_managers[index]

    def start_device_managers(self):
        for device_manager in self.device_managers:
            device_manager.start()
            # print(f"camer id : {device_manager.device.get_info(rs.camera_info.serial_number)} started")        

    def close_rs2_device(self):
        for device_manager in self.device_managers:
            device_manager.stop()
            # print(f"camer id : {device_manager.device.get_info(rs.camera_info.serial_number)} stopped")
