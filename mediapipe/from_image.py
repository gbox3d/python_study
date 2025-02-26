#%%
import cv2
import mediapipe as mp


from IPython.display import display
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageColor as ImageColor
import PIL.Image as Image

# 다운로드한 face_landmarker.task 파일의 절대 경로
model_path = "./face_landmarker_v2_with_blendshapes.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


# 이미지 모드 설정 (단일 이미지 처리)
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    output_face_blendshapes=True,              # 얼굴 블렌드셰이프 출력 여부
    output_facial_transformation_matrixes=True   # 얼굴 변환 행렬 출력 여부
)

landmarker = FaceLandmarker.create_from_options(options)

print(f"FaceLandmarker 생성 완료: {landmarker}")
#%%
# 예시 이미지 로드 (BGR 형식)
image = cv2.imread("image.png")
if image is None:
    raise ValueError("이미지 파일을 찾을 수 없습니다.")

# MediaPipe Image 객체로 변환 (RGB 형식 사용)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# 얼굴 랜드마킹 수행
result = landmarker.detect(mp_image)

# 결과 출력 (예: 랜드마크 좌표, 블렌드셰이프 등)
print("Face Landmarker Result:")
print(result)

# %% face landmark 출력

# 이미지 크기 구하기
height, width = image.shape[:2]
output_image = image.copy()

# 첫 번째 얼굴의 모든 랜드마크에 대해 좌표 계산 후 그리기
for landmark in result.face_landmarks[0]:
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    cv2.circle(output_image, (x, y), radius=2, color=(0, 255, 0), thickness=-1)
display(Image.fromarray(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)))


# %% facial transformation matrix 출력
# 얼굴 변환 행렬 정보만 출력
if result.facial_transformation_matrixes:
    print("얼굴 트랜스폼 정보:")
    for matrix in result.facial_transformation_matrixes:
        print(matrix)
else:
    print("얼굴 트랜스폼 정보가 없습니다.")


# %%
face_landmarks = result.face_landmarks[0]
parts = {
            'right_eye': face_landmarks[468],
            'left_eye': face_landmarks[473],
            'nose': face_landmarks[4],
            'up_mouth': face_landmarks[0],
            'bottom_mouth': face_landmarks[17]
        }

print(parts["right_eye"])



# %%
height, width = image.shape[:2]
output_image = image.copy()

for name,part in parts.items():
    x = int(part.x * width)
    y = int(part.y * height)
    cv2.circle(output_image, (x, y), 3, (0, 255, 0), -1)
    cv2.putText(output_image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
display(Image.fromarray(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)))




# %%
