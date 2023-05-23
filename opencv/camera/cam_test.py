import cv2 as cv
import argparse

# argparse 객체 생성
parser = argparse.ArgumentParser()

# 인자 추가
parser.add_argument("-W", type=int, default=640, help="넓이 (기본값: 640)")
parser.add_argument("-H", type=int, default=480, help="폭 (기본값: 480)")
parser.add_argument("-C", type=int, default=0, help="카메라 선택 기본값: 0")

# 커맨드 라인에서 인자 파싱
args = parser.parse_args()

# 넓이, 폭, 카메라 선택 출력
print("넓이:", args.W)
print("폭:", args.H)
print("카메라 선택:", args.C)

cap = cv.VideoCapture(args.C)

#set camera 
cap.set(cv.CAP_PROP_FRAME_WIDTH, args.W)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, args.H)
# cap.set(cv.CAP_PROP_FPS, 30)

#get fps
print(f'fps : {cap.get(cv.CAP_PROP_FPS)}')

while(True) :
    ret,frame = cap.read()

    cv.imshow('frame',frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
cap.release()
cv.destroyAllWindows()