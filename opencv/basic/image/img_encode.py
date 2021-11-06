#%%
import numpy as np
import cv2 as cv
import io

#%%비트멥 만들기 
img = np.zeros((512,512,3),np.uint8)

#%%텍스트 출력 
font = cv.FONT_HERSHEY_SIMPLEX
_ = cv.putText(img,'OpenCV ',(10,500), font, 0.5,(255,255,255),2,cv.LINE_AA)

print(_.shape)

#%% 직접 encode 인코딩해서 저장하기
encode_param=[int(cv.IMWRITE_JPEG_QUALITY),90]
_,_encodee_img = cv.imencode('.jpg',img,encode_param)

with open('./test.jpg','wb') as fd :
    fd.write( _encodee_img.tobytes() )

#%%

# cv.imwrite('./test.png',img)

print("save ok..")
# %%
