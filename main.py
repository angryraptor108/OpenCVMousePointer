import cv2
#import mouse
import pyautogui as pyatogui
import numpy as np
import pynput
import time

from cvzone.HandTrackingModule import HandDetector

def get_slope(p1, p2) -> float:
    x1, y1 = p1
    x2, y2 = p2

    if (x2-x1) != 0:
        return ((y1-y2)/(x2-x1))
    else:
        return 1000

detector_hand = HandDetector(detectionCon=0.9, maxHands=1)
last_click_time = time.monotonic() # keep track of time since last mouse click
last_keyboard_time = time.monotonic() # keep track of time since last keyboard click

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


        #x, y, z = lmlist[8]

        #print(lmlist[8])
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
            length, lineInfo, img = detector_hand.findDistance(lmlist[8][::2], lmlist[4][::2], img)
            
            #print(length)
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255, 255, 0), cv2.FILLED)

            if length > 30:
                if time.monotonic() - last_click_time >= 1: # prevent spam clicking
                    pynput.mouse.Controller().click(pynput.mouse.Button.left)
                    last_click_time = time.monotonic()
        
        if fingers[1] == 1 and fingers[2] == 1:
            slope = get_slope(lmlist[5][::2], lmlist[8][::2])
            #print(slope)

            if (slope < 0.8) and (slope > 0.1) and (time.monotonic() - last_keyboard_time >= 1): # swipe right
                pyatogui.keyDown('ctrl')
                pyatogui.press('right')
                pyatogui.keyUp('ctrl')
                last_keyboard_time = time.monotonic()
            elif (slope < -0.1) and (slope >-0.8) and (time.monotonic() - last_keyboard_time >= 1):
                pyatogui.keyDown('ctrl')
                pyatogui.press('left')
                pyatogui.keyUp('ctrl')
                last_keyboard_time = time.monotonic()

        
        #distance = ((lmlist[8][0] - lmlist[5][0])**2 + (lmlist[8][1] - lmlist[5][1])**2)**0.5
        #print(distance)


    cv2.imshow('camera feed', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()