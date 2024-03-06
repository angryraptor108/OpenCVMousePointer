import cv2
#from cvzone.HandTrackingModule import HandDetector

#detector = HandDetector(detectionCon=0.9, maxHands=1)

cap = cv2.VideoCapture(0)

cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)

while True:
    sucess, img = cap.read() 
    if not sucess:
        break
    img = cv2.flip(img, 1)
    #hands, img = detector.findHands(img, flipType=False)



    cv2.imshow('camera feed', img)
    cv2.waitKey(1)
