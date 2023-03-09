"""
해당 코드는 이미지 처리를 위해 파이썬에서 OpenCV 및 PIL 라이브러리를 사용하였습니다. 
이 코드는 이미지를 불러오고, 일부를 자른 후, 원근 변환을 적용하여 이미지를 변환하고 변환된 이미지를 표시합니다.

원근 변환을 위해 getPerspectiveTransform() 및 warpPerspective() 함수를 사용하였습니다. 
getPerspectiveTransform() 함수는 원본 이미지에서 좌표를 선택하여 목표 이미지에서 그 좌표를 어떻게 변환할지 결정하는 원근 변환 행렬을 계산합니다. 
warpPerspective() 함수는 이미지를 변환하고 출력 이미지를 반환합니다.
이 코드에서는 cv2.imread() 함수를 사용하여 이미지를 불러오고, numpy 배열 형태로 변환합니다. 이후 PIL.Image.fromarray() 함수를 사용하여 이미지를 출력합니다. 이어서, numpy 배열의 슬라이싱을 사용하여 이미지 일부를 자릅니다. getPerspectiveTransform() 함수를 사용하여 변환 행렬(M)을 계산하고, warpPerspective() 함수를 사용하여 변환된 이미지를 반환합니다. 마지막으로, PIL.Image.fromarray() 함수를 사용하여 변환된 이미지를 출력합니다.
이러한 원근 변환은 카메라 각도로 인해 발생하는 원근 왜곡을 보정하고, 이미지 내의 객체가 다른 각도에서 본 것처럼 보이도록 하는 데 유용합니다.
"""
#%%
import cv2
import numpy as np 

import PIL.Image as Image
from IPython.display import display
#%% 고수준 로더 사용 
img = cv2.imread('../../IMG_5730.jpeg')
display(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
# %%

_img = img[1000:1950, 400:1900]

display(Image.fromarray(cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)))

# %%
h, w = _img.shape[:2]
print(h, w)
# 변환 행렬 구하기
#원래 이미지의 좌측 상단, 우측 상단, 우측 하단, 좌측 하단 순서로 좌표를 지정하여 src_pts에 저장하였습니다. 
src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]) 
#변환된 이미지의 좌측 상단, 우측 상단, 우측 하단, 좌측 하단 순서로 좌표를 지정하여 dst_pts에 저장하였습니다.
dst_pts = np.float32([[0, 0], [w, 0], [int(0.85*w), h], [int(0.15*w), h]])
M = cv2.getPerspectiveTransform(src_pts, dst_pts)
print(M)

# 이미지 원근 변환 수행
warped_img = cv2.warpPerspective(_img, M, (w, h))

#%%
display(Image.fromarray(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)))
# %%
