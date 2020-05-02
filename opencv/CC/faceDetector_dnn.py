#python3 faceDetector_dnn.py --image test_image.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python3 faceDetector_dnn.py --image ../res/cascade/2.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

# importing necessary packages
import numpy as np
import argparse
import cv2 as cv


print(cv.__version__)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True, help="patho to input image")
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffee 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")

args = vars(ap.parse_args())

# load model from disk
print("[INFO] loading from model...")
net = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and construct an input blob for the image and resize image to
# fixed 300x300 pixels and then normalize it
image = cv.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv.dnn.blobFromImage(cv.resize(image, (300,300)), 1.0, (300, 300), (103.93, 116.77, 123.68))

# pass the blob through the network and obtain the detections and
# predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

print(detections.shape[2])
# loop over the detections
for i in range(0, detections.shape[2]):
    # extract the confidence (i.e., probability) associated with the
    # prediction
    confidence = detections[0, 0, i, 2]

    # filter out weak detections by ensuring the `confidence` is
    # greater than the minimum confidence
    if confidence > args["confidence"]:
        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the bounding box of the face along with the associated
        # probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv.rectangle(image, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv.putText(image, text, (startX, y),
                    cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

cv.imshow('img',image)
cv.waitKey(0)
cv.destroyAllWindows()
