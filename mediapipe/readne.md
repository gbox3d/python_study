## setup

task file download
```bash
wget -O face_landmarker_v2_with_blendshapes.task -q https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

## land mark

```python
parts = {
            'right_eye': face_landmarks[468],
            'left_eye': face_landmarks[473],
            'nose': face_landmarks[4],
            'up_mouth': face_landmarks[0],
            'bottom_mouth': face_landmarks[17]
        }
```
