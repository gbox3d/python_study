"""
Hand Tracing Module
By: Murtaza Hassan
mod by gbox3d , 2021.5.10
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.murtazahassan.com/
"""

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                cz = 1

                if lm.z < 0 :
                    cz = int(lm.z * 50) * -1
                
                
                # print(id, cx, cy)
                # if lm.z > 20 :
                #     cz = lm.z / 20 
                # else:
                #     cz = 10
                # print(cz)
                lmList.append([id, cx, cy,lm.z])
                if draw:
                    cv2.circle(img, (cx, cy), cz, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    detector = handDetector()
    while True:
        success, img = cap.read()

        img = detector.findHands(cv2.flip(img,1))
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
