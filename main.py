import cv2
#import mouse
import pyautogui as pyatogui
import numpy as np
import pynput

from cvzone.HandTrackingModule import HandDetector

detector_hand = HandDetector(detectionCon=0.9, maxHands=1)

cap = cv2.VideoCapture(0)

cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)

frameR = 100 # frame reduction value

while True:
    #print(pyatogui.position())
    pyatogui.PAUSE = 0.00
    
    sucess, img = cap.read() 
    if not sucess:
        break
    img = cv2.flip(img, 1)
    hands, img = detector_hand.findHands(img, flipType=False, draw=True)
    cv2.rectangle(img, (frameR, frameR), (cam_w-frameR, cam_h-frameR), (255, 0, 255), 2)

    if hands:
        #print(hands[0])
        lmlist = hands[0]['lmList']
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        thum_x, thum_y = lmlist[4][0], lmlist[4][1]
        cv2.circle(img, (ind_x, ind_y), 5, (255, 0, 255), 2)

        fingers = detector_hand.fingersUp(hands[0])
        #print(fingers)

        # mouse movement
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:
            #print("mouse (x,y): (" + str(ind_x) + ",", str(ind_y) + ")")
            conv_x = int(np.interp(ind_x, [frameR, cam_w-frameR], [0, 1920])) #subtracting frame reduction to avoid jitter
            conv_y = int(np.interp(ind_y, [frameR, cam_h-frameR], [0, 1080]))
            pynput.mouse.Controller().position = (conv_x, conv_y)
            
            #pyatogui.moveTo(conv_x, conv_y, 0.1) #using pyautogui to move mouse instead of mouse because macOS doesn't support mouse
            #mouse.move(conv_x, conv_y) #using mouse gives Darwin erorr on macOS


        # FIX THIS
        #if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
            #length, img, lineInfo = detector_hand.findDistance(lmlist[8], lmlist[4], img)
            
            
            #print(length)
            #if length < 30:
                #cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                #pyatogui.click()
        
        #distance = ((lmlist[8][0] - lmlist[5][0])**2 + (lmlist[8][1] - lmlist[5][1])**2)**0.5
        #print(distance)


    cv2.imshow('camera feed', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()