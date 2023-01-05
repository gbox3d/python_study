#%%
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
camera_fps = int(cap.get(cv2.CAP_PROP_FPS))

print(f'camera width : {camera_width} , camera height : {camera_height}, camera fps : {camera_fps}')

#%%
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
vid_writer = cv2.VideoWriter('output.mp4', fourcc, 
                             camera_fps, 
                             (camera_width, camera_height))

#%%
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.flip(frame,0)
        # resize_frame = cv2.resize(frame, (640, 480))
        
        vid_writer.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
cap.release()
vid_writer.release()

cv2.destroyAllWindows()