import cv2
#import mouse
import pyautogui as pyatogui

from cvzone.HandTrackingModule import HandDetector

detector_hand = HandDetector(detectionCon=0.9, maxHands=1)

cap = cv2.VideoCapture(0)

cam_w, cam_h = 1920, 1080
cap.set(3, cam_w)
cap.set(4, cam_h)

while True:
    #print(pyatogui.position())
    
    sucess, img = cap.read() 
    if not sucess:
        break
    img = cv2.flip(img, 1)
    hands, img = detector_hand.findHands(img, flipType=False)
    if hands:
        lmlist = hands[0]['lmList']
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        cv2.circle(img, (ind_x, ind_y), 5, (255, 0, 255), 2)
        print("mouse (x,y): (" + str(ind_x) + ",", str(ind_y) + ")")
        pyatogui.moveTo(ind_x, ind_y, 0.1)


    cv2.imshow('camera feed', img)
    cv2.waitKey(1)
