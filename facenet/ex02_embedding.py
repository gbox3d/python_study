#%%
import torch
from torchvision.transforms import ToTensor
from torchvision.transforms import ToPILImage
from torchvision.transforms import Resize

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display
import numpy as np

# MTCNN 모델 로드
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f'Using device: {device} ')

mtcnn = MTCNN(keep_all=True, device=device)
print("MTCNN 모델 로드 완료")

# FaceNet 모델 로드
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
print("FaceNet 모델 로드 완료")


#%%
# 멤버 이미지 임베딩 생성
# def get_embedding(image_path):
#     image = Image.open(image_path)
#     face, _ = mtcnn(image, return_prob=True)
#     if face is not None:
#         face = face[0].unsqueeze(0).to(device)
#         embedding = resnet(face).detach().cpu().numpy()
#         return embedding
#     else:
#         raise ValueError(f"얼굴을 찾을 수 없습니다: {image_path}")

# 유사도 계산 함수
def cosine_similarity(vec1, vec2):
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)
    return np.dot(vec1, vec2)

#%%
# 이미지 읽기 및 멤버 임베딩 생성
member_image_path = "moon_sh.jpg"
group_image_path = "55.jpg"

image = Image.open(member_image_path)
face, _ = mtcnn(image, return_prob=True)

# 얼굴 텐서에서 정규화 값 복원
face_tensor = face[0]
face_image = ((face_tensor.permute(1, 2, 0).detach().numpy() + 1) * 127.5).astype(np.uint8)  # -1~1에서 0~255로 변환
face_pil = Image.fromarray(face_image)  # PIL 이미지로 변환

# 표시
display(face_pil)
print("기준 이미지")

if face is not None:
    face = face[0].unsqueeze(0).to(device)
    embedding = resnet(face).detach().cpu().numpy()
    member_embedding = embedding
    
    
else:
    raise ValueError(f"얼굴을 찾을 수 없습니다: {member_image_path}")


#%%

# 그룹 이미지에서 얼굴 감지 및 유사도 계산
group_image = Image.open(group_image_path)
boxes, probs = mtcnn.detect(group_image)


def prewhiten(img):
    mean = np.mean(img)
    std = np.std(img)
    std_adj = np.maximum(std, 1.0 / np.sqrt(img.size))
    return (img - mean) / std_adj

#%%

# 폰트 설정
font_size = 64  # 원하는 텍스트 크기
try:
    font = ImageFont.truetype("arial.ttf", font_size)  # Arial 폰트를 사용하는 경우
    print("Arial 폰트를 사용합니다.")
except IOError:
    font = ImageFont.load_default()  # Arial 폰트를 못 찾으면 기본 폰트를 사용
    print("기본 폰트를 사용합니다.")



#%%
if boxes is not None:
    draw = ImageDraw.Draw(group_image)
    for box, prob in zip(boxes, probs):
        face = group_image.crop((box[0], box[1], box[2], box[3]))
        
        
        
        # 얼굴 이미지를 (160, 160) 크기로 조정
        face_resized = face.resize((160, 160))
        
        # PIL 이미지를 numpy 배열로 변환 후 텐서 변환
        face_tensor = ToTensor()(face_resized).unsqueeze(0).to(device)
        
        # 얼굴 임베딩 생성
        face_embedding = resnet(face_tensor).detach().cpu().numpy()
        print(f"Face embedding shape: {face_embedding.shape}")
        print(f"member_embedding shape: {member_embedding.shape}")
       
        # 유사도 계산
        # similarity = cosine_similarity(member_embedding, face_embedding)
        # 유사도 계산 전 1차원 벡터로 변환
        similarity = cosine_similarity(member_embedding.flatten(), face_embedding.flatten())

        # 박스 및 유사도 표시
        draw.rectangle(box.tolist(), outline=(255, 0, 0), width=3)
        draw.text((box[0], box[1] - 10), f"{similarity:.2f}", fill=(255, 255, 0), font=font)
        
        display(face)
        print(f"유사도: {similarity:.2f}")

    # 결과 출력
    display(group_image)
    group_image.save("result.jpg")
else:
    print("그룹 이미지에서 얼굴을 감지할 수 없습니다.")
# %%
