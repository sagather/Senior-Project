import cv2
#for motion detection
import argparse
import datetime
import imutils
import time
import numpy as np

#Referenced for motion detection: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

#Might be needed later
    # feedWidth = originalFeed.get(3)
    # feedHeight = originalFeed.get(4)

# Load in cascade files
face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
leftEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_lefteye_2splits.xml')
rightEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_righteye_2splits.xml')

originalFeed = cv2.VideoCapture(0)


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

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

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)


#Face Detection
    facesDetected = face_cascade.detectMultiScale(gray, 1.3, 5)
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

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = eye_cascade.detectMultiScale(roiGray)
        for (ex,ey,ew,eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex+ew, ey+eh), (0,255,0), 1)

        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < args["min_area"]:
                continue

            (mx, my, mw, mh) = cv2.boundingRect(c)
            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (244, 66, 232), 2)
            #text = "Motion Detected"

            # Something Like this to check for specific motion?
            if mx < x and my < y:
                text = "Motion Top left"
            elif mx > x and my > y:
                text = "                Motion Top Right"


            # draw the text and timestamp on the frame
            # may not be needed, but may be useful for Sam
            cv2.putText(frame, "Frame Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # blue box = faces, green = eyes, red = left eyes, white = right eyes
    cv2.imshow("preview", frame)
    cv2.imshow("grayFeed", gray);

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

originalFeed.release()
cv2.destroyAllWindows()