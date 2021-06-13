#%% video sample for mp4
import cv2 as cv
import numpy as np

from PIL import Image
from IPython.display import display

print( f"opencv version : {cv.__version__}")

#%% 한프레임씩 읽어서 출력하기 
cap = cv.VideoCapture('../../res/akb48_heart_gatavirus.mp4')
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
