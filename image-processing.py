#All import statements

import cv2
#for motion detection
import argparse
import datetime
import imutils
import time
import numpy as np

#Referenced for motion detection: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

#Might be needed later
#   _feedWidth = originalFeed.get(3)
#   _feedHeight = originalFeed.get(4)

# Load in cascade files
_face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
_eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
_leftEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_lefteye_2splits.xml')
_rightEye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_righteye_2splits.xml')

_originalFeed = cv2.VideoCapture(0)

_ap = argparse.ArgumentParser()
_ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
_args = vars(_ap.parse_args())

_firstFrame = None;
_frameText = ""

#TODO:  GET FIRST FRAME FUNCTION
def firstFrame():

    if _originalFeed.isOpened():  # try to get the first frame
        rval, frame = _originalFeed.read()
        _frameText = "No Motion"
        return rval;


#TODO:  PUT TEXT INTO FRAME



#TODO: FACE DETECTION FUNTCION



#TODO:  MAIN FUNCTION

while rval:
    rval, frame = _originalFeed.read()

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < _args["min_area"]:
            continue

        (mx, my, mw, mh) = cv2.boundingRect(c)
        cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (244, 66, 232), 2)
        text = "Motion Detected"

        # draw the text and timestamp on the frame
        #may not be needed, but may be useful for Sam
        cv2.putText(frame, "Frame Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

