import cv2
import numpy as np

# Load in cascade files
face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
leftEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_lefteye_2splits.xml')
rightEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_righteye_2splits.xml')

originalFeed = cv2.VideoCapture(0)

if originalFeed.isOpened():  # try to get the first frame
    rval, frame = originalFeed.read()
else:
    rval = False

while rval:
    rval, frame = originalFeed.read()

    grayFeed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facesDetected = face_cascade.detectMultiScale(grayFeed, 1.3, 5)
    for (x,y,w,h) in facesDetected:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        roiGray = grayFeed[y:y+h, x:x+w]
        roiColor = frame[y:y+h, x:x+w]

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = eye_cascade.detectMultiScale(roiGray)
        for (ex,ey,ew,eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex+ew, ey+eh), (0,255,0), 1)
        # Detect left eyes
        leftEyesDetected = leftEye_cascade.detectMultiScale(roiGray)
        for (ex, ey, ew, eh) in leftEyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
        # detect right eyes
        rightEyesDetected = rightEye_cascade.detectMultiScale(roiGray)
        for (ex, ey, ew, eh) in rightEyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex + ew, ey + eh), (255, 255, 255), 1)

    # blue box = faces, green = eyes, red = left eyes, white = right eyes
    cv2.imshow("preview", frame)


    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

originalFeed.release()
cv2.destroyAllWindows()