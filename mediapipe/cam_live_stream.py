import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class LiveStreamFaceLandmarker:
    detection_fps = 0
    def __init__(self, model_path):
        # 콜백에서 참조할 결과 저장용 변수를 준비
        self.last_result = None
        
        # 콜백 함수 정의
        def face_landmarker_callback(
            result: vision.FaceLandmarkerResult, 
            output_image: mp.Image, 
            timestamp_ms: int
        ):
            # 비동기로 계산된 결과가 이 콜백으로 들어옴
            self.last_result = result
            #update detection fps
            self.detection_fps = 1 / (time.time() - timestamp_ms / 1000)
        
        # 옵션 설정
        base_options = python.BaseOptions(
            model_asset_path=model_path,
            #delegate=python.BaseOptions.Delegate.GPU # window아직 미구현
            )
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,   # 라이브 스트림 모드
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1,
            # 콜백 함수 등록
            result_callback=face_landmarker_callback
        )
        # FaceLandmarker 생성
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect_async(self, mp_image, timestamp_ms):
        # 비동기 호출 -> 결과는 콜백으로 온다
        self.detector.detect_async(mp_image, timestamp_ms=timestamp_ms)
        

#
# 실제 사용 예시
#
model_path = "./mediapipe/face_landmarker_v2_with_blendshapes.task"
landmarker = LiveStreamFaceLandmarker(model_path)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # MediaPipe는 RGB 입력을 권장
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # 타임스탬프(ms 단위)는 자유롭게 지정 가능(아래는 예시로 Unix time * 1000 사용)
    timestamp_ms = int(time.time() * 1000)

    # 비동기 감지 요청 -> 결과는 콜백에서 landmarker.last_result로 저장
    landmarker.detect_async(mp_image, timestamp_ms)

    # 콜백에서 저장된 결과를 메인 루프에서 사용
    if landmarker.last_result and landmarker.last_result.face_landmarks:
        face_landmarks = landmarker.last_result.face_landmarks[0]
        h, w, _ = frame.shape
        
        parts = {
            'right_eye': face_landmarks[468],
            'left_eye': face_landmarks[473],
            'nose': face_landmarks[4],
            'up_mouth': face_landmarks[0],
            'bottom_mouth': face_landmarks[17]
        }
        
        for name,part in parts.items():
            x = int(part.x * w)
            y = int(part.y * h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
    cv2.putText(frame, f"FPS: {landmarker.detection_fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        

    cv2.imshow("Face Landmarker - LIVE_STREAM Callback", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # q or esc key
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
