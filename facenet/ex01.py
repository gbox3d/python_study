#%%
# import cv2 as cv
import torch
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw
from IPython.display import display


#%%
# MTCNN 모델 로드
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)


#%%
# 이미지 읽기
image_path = "55.jpg"
image = Image.open(image_path)

#이미지 display로 출력 해보기
display(image)


#%%
# 얼굴 감지
boxes, _ = mtcnn.detect(image)

# 결과 출력 (네모 박스 그리기)
if boxes is not None:
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle(box.tolist(), outline=(255, 0, 0), width=3)

display(image)
# 결과 저장
# output_path = "result.jpg"
# image.save(output_path)

# print(f"결과 이미지가 저장되었습니다: {output_path}")

# %%
