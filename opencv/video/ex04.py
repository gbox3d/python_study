#%% video sample for mp4
import cv2 as cv
import numpy as np

from PIL import Image
from IPython.display import display

print( f"opencv version : {cv.__version__}")

#%% 같은 비율로 크기 변경, 남은 공간에 테드리색 넣기
def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 32), np.mod(dh, 32)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)

#%% 한프레임씩 읽어서 출력하기 
cap = cv.VideoCapture('../res/akb48_heart_gatavirus.mp4')
total_framecount = int(cap.get(cv.CAP_PROP_FRAME_COUNT)) # 전체 프레임 구하기 

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print(f'total frame count {total_framecount}')
print(f'width : {frame_width}')
print(f'height : {frame_height}')

#%%
if cap.isOpened() :
    
    cap.set(cv.CAP_PROP_POS_FRAMES,0) #프레임 선택

    ret, frame = cap.read()
    img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    display( Image.fromarray(img_rgb) )

    cap.set(cv.CAP_PROP_POS_FRAMES,100) # 100 프레임 
    ret, frame = cap.read()
    img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    display( Image.fromarray(img_rgb) )
    cap.release()



# if cap.isOpened() :
#     while(True):
#         ret, frame = cap.read()
#         if frame is None :
#             break
        
#         _img = letterbox(frame,new_shape=(640,640))[0]
#         cv.imshow('frame',_img)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()

# cv.destroyAllWindows()


# %%
