import cv2
#for motion detection
import argparse
import datetime
import imutils
import time
import numpy as np
from Person import Person

#Referenced for motion detection: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

#Might be needed later
    # feedWidth = originalFeed.get(3)
    # feedHeight = originalFeed.get(4)

# Load in cascade files
face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')

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

    # Array to hold motion states of quadrants
    motion = [0,0,0,0]
    # List to hold people detected in frame
    people = []
    # i to serve as an index when going through faces
    i = 0

#Face Detection
    facesDetected = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in facesDetected:

        # Add new person to people list if face detected
        people.append(Person())
        currentPerson = people[i]

        # Lazy way to change color
        if i == 0:
            Person.setColor(people[i], 255, 0, 0) # Blue for 1st face
        if i == 1:
            Person.setColor(people[i], 0, 255, 255) # Yellow for 2nd face
        if i == 2:
            Person.setColor(people[i], 255, 255, 0) # Teal for 3rd face
        if i == 3:
            Person.setColor(people[i], 0, 100, 255) # Orange for 4th face

        cv2.rectangle(frame, (x,y), (x+w, y+h), (currentPerson.color[0], currentPerson.color[1], currentPerson.color[2]), 2)
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

        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        i += 1

        for c in cnts:
            if cv2.contourArea(c) < args["min_area"]:
                continue

            (mx, my, mw, mh) = cv2.boundingRect(c)

            #coordinates for the smaller boxes
            nx = mx + (mw / 4)
            ny = my + (mh / 4)
            nz = mx + mw - (mw / 4)
            na = my + mh - (mh / 4)

            #rectangle must be in detection zones and smaller than detection area (I think)
            if (nx >= x-(2*w) and nx <= x+(2*w)+w) and (ny >= y and ny <= y+(4*h)) \
                    and (nz >= x-(2*w) and nz <= x+(2*w)+w) and (na >= y and na <= y+(4*h)) \
                    and (mw <= ((x+(2*w)+w) - (x-(2*w))) and mh <= (y+(4*h) - y)):
                cv2.rectangle(frame, (nx, ny), (nz, na), (244, 66, 232), 2)
                #cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (244, 66, 232), 2)
            #text = "Motion Detected"

            # Something Like this to check for specific motion?
            if (nx >= x-(2*w) and nx <= x+(w/2)) and (ny >= y and ny <= y+(2*h)):
                text = "                    Motion Top Right"
                motion[1] = 1
            elif (nx <= x+(2*w)+w) and (nx >= x+(w/2)) and (ny >= y and ny <= y+(2*h)):
                text = "Motion Top Left"
                motion[0] = 1
            elif (nx >= x-(2*w) and nx <= x+(w/2)) and (ny >= y + (2 * h) and ny <= y + (4 * h)):
                text = "                    Motion Bottom Right"
                motion[3] = 1
            elif (nx <= x+(2*w)+w) and (nx >= x+(w/2)) and (ny >= y+(2*h) and ny <= y+(4*h)):
                text = "Motion Bottom Left"
                motion[2] = 1

            if motion[0] == 1 and motion[1] == 1:
                text = "    Motion BOTH Top"
            if motion[2] == 1 and motion[3] == 1:
                text = "    Motion BOTH Bottom"

    # blue box = faces, green = eyes, red = left eyes, white = right eyes

    # Flip frame then add text
    horizontal = cv2.flip(frame, 1)

    # draw the text and timestamp on the frame
    # may not be needed, but may be useful for Sam
    cv2.putText(horizontal, "Frame Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(horizontal, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.putText(horizontal, "Faces in frame: {}".format(len(people)), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("preview", horizontal)
    cv2.imshow("grayFeed", gray);

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

originalFeed.release()
cv2.destroyAllWindows()