import cv2
import mediapipe as mp


def fingerQuantification(leftLmList, rightLmList):
    rightFinger = []
    leftFinger = []
    if len(rightLmList) > 0:
        rightFingerOptions = [rightLmList[4][1] - rightLmList[2][1], rightLmList[6][2] - rightLmList[8][2],
                              rightLmList[10][2] - rightLmList[12][2],
                              rightLmList[14][2] - rightLmList[16][2], rightLmList[18][2] - rightLmList[20][2]]

        for fingerPos in rightFingerOptions:
            if fingerPos > 0:
                rightFinger.append(1)
            else:
                rightFinger.append(0)

    if len(leftLmList) > 0:
        leftFingerOptions = [leftLmList[2][1] - leftLmList[4][1], leftLmList[6][2] - leftLmList[8][2],
                             leftLmList[10][2] - leftLmList[12][2],
                             leftLmList[14][2] - leftLmList[16][2], leftLmList[18][2] - leftLmList[20][2]]

        for fingerPos in leftFingerOptions:
            if fingerPos > 0:
                leftFinger.append(1)
            else:
                leftFinger.append(0)
    return leftFinger, rightFinger


class handDetector():
    def __init__(self, mode=False, upper_body_only=True, smooth_landmarks=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.holistic = mp.solutions.holistic
        self.landmarks = self.holistic.Holistic(self.mode, self.upper_body_only, self.smooth_landmarks, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img.flags.writeable = True
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.landmarks.process(imgRGB)

        if self.results.left_hand_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.left_hand_landmarks, self.holistic.HAND_CONNECTIONS)
        if self.results.right_hand_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.right_hand_landmarks, self.holistic.HAND_CONNECTIONS)
        return img

    def leftFindPosition(self, img, draw=True):
        lmList = []
        if self.results.left_hand_landmarks:
            myHand = self.results.left_hand_landmarks
            h, w, c = img.shape
            for i in range(len(myHand.landmark)):
                cx, cy = int(myHand.landmark[i].x * w), int(myHand.landmark[i].y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def rightFindPosition(self, img, draw=True):
        lmList = []
        if self.results.right_hand_landmarks:
            myHand = self.results.right_hand_landmarks
            h, w, c = img.shape
            for i in range(len(myHand.landmark)):
                cx, cy = int(myHand.landmark[i].x * w), int(myHand.landmark[i].y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList