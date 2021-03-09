#%% video sample for mp4
import cv2
import numpy as np

from IPython.display import display
print( f"opencv version : {cv2.__version__}")

#%% arguments
import argparse

parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument('--id', type=str, 
    help='help : input id')
parser.add_argument('--ip', type=str, 
    help='help : input ip')
parser.add_argument('--passwd', type=str, 
    help='help : pass word')


_args = parser.parse_args()

url = f'rtsp://{_args.id}:{_args.passwd}@{_args.ip}:554/stream_ch00_0'
print(url)


#%% 한프레임씩 읽어서 출력하기 
#https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv
cap = cv2.VideoCapture(url)

if cap.isOpened() :
    while(True):
        ret, frame = cap.read()
        if frame is None :
            break
        # _img = letterbox(frame,new_shape=(640,640))[0]
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

cv2.destroyAllWindows()

