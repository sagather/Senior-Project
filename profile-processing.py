import cv2
import argparse
import datetime
import imutils

# Load in cascade files
face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_profileface.xml')
originalFeed = cv2.VideoCapture(0)

firstFrame = None;

if originalFeed.isOpened():  # try to get the first frame
    rval, frame = originalFeed.read()
    text = "No Motion"

while rval:
    rval, frame = originalFeed.read()

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

#Face Detection
    facesDetected = face_cascade.detectMultiScale(gray, 1.1, 5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in facesDetected:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        #Top
        cv2.rectangle(frame, (x+(w/2),y), (x-(2*w), y+(2*h)), (0, 255, 0), 2) #To the left of face as displayed on  (Green)
        cv2.rectangle(frame, (x+(w/2),y), (x+(2*w)+w, y+(2*h)), (0, 0, 255), 2) #To the right of face as displayed on webcam (Red)
        #Bottom
        cv2.rectangle(frame, (x+(w/2),y+(2*h)), (x+(2*w)+w, y+(4*h)), (0, 255,0), 2) #To the left of face as displayed on webcam (Green)
        cv2.rectangle(frame, (x+(w/2),y+(2*h)), (x-(2*w), y+(4*h)), (0, 0,255), 2) #To the right of face as displayed on webcam

        roiGray = gray[y:y+(h/2), x:x+w]
        roiColor = frame[y:y+h, x:x+w]

        cv2.imshow("roiGray", roiGray);
        cv2.imshow("roiColor", roiColor);

    # Flip frame then add text
    horizontal = cv2.flip(frame, 1)

    cv2.imshow("preview", horizontal)
    cv2.imshow("grayFeed", gray);

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

originalFeed.release()
cv2.destroyAllWindows()