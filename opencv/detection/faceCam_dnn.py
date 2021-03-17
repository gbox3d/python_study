#python3 faceCam_dnn.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
import cv2 as cv
import sys 
import time

import numpy as np
import argparse

print(cv.__version__)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-v", "--videodevice", type=int,default=0, help="video device id default(0)")
ap.add_argument("--videoWidth", type=int,default=640, help="video width")
ap.add_argument("--videoHeight", type=int,default=480, help="video height")
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffee 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")

args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
net = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])

cap = cv.VideoCapture(args["videodevice"])

if cap.get(3) < 10 : 
    print('not found cam')
    exit()
else : 
    print(f'found cam : {cap.get(3),{cap.get(4)}}') 
    cap.set(3,args["videoWidth"])
    cap.set(4,args["videoHeight"])
    time.sleep(1)
    print(f'change resolution : {cap.get(3),{cap.get(4)}}') 


while(True) :
    # time.sleep(1)

    ret,frame = cap.read()

    (h, w) = frame.shape[:2]
    blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 1.0, (300, 300), (103.93, 116.77, 123.68))

    # pass the blob through the network and obtain the detections and predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence < args["confidence"]:
            continue

        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the bounding box of the face along with the associated
        # probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv.rectangle(frame, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv.putText(frame, text, (startX, y),
                    cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # show the output frame
    cv.imshow("Face detector from camera stream", frame)

    _k = cv.waitKey(1) & 0xff
    if _k == 27 : break
    # if cv.waitKey(1) & 0xFF == ord('q') :
        # break

cap.release()
cv.destroyAllWindows()
