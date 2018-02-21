#All import statements

import cv2
#for motion detection
import argparse
import datetime
import imutils

#unnecessary, may be removed in later versionings
import time
import numpy as np

#Referenced for motion detection: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

#Might be needed later
#   _feedWidth = originalFeed.get(3)
#   _feedHeight = originalFeed.get(4)

# Load in cascade files
_face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
_eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')

_originalFeed = cv2.VideoCapture(0)

_ap = argparse.ArgumentParser()
_ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
_args = vars(_ap.parse_args())

_firstFrame = None;
_grayFrame = None;
_frameText = "";

#TODO:  GET FIRST FRAME FUNCTION
def firstFrame():
    if _originalFeed.isOpened():  # try to get the first frame
        rval, frame = _originalFeed.read()
        _frameText = "No Motion"
        return rval;


#TODO:  PUT TEXT INTO FRAME
def updateFrameStatusTextOnFrame(statusStr):
    cv2.putText(frame, "Frame Status: {}".format(statusStr), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def updateTimestampTextOnFrame():
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


#TODO: FACE DETECTION FUNTCION
def faceDetect():
    facesDetected = _face_cascade.detectMultiScale(gray, 1.3, 5);
    for (x,y,w,h) in facesDetected:
        cv2.rectangle(_firstFrame, (x,y), (x+w, y+h), (255,0,0), 2);
        #Top
        cv2.rectangle(_firstFrame, (x+(w/2),y), (x-(2*w), y+(2*h)), (0, 255, 0), 2); #To the left of face as displayed on  (Green)
        cv2.rectangle(_firstFrame, (x+(w/2),y), (x+(2*w)+w, y+(2*h)), (0, 0, 255), 2); #To the right of face as displayed on webcam (Red)
        #Bottom
        cv2.rectangle(_firstFrame, (x+(w/2),y+(2*h)), (x+(2*w)+w, y+(4*h)), (0, 255,0), 2); #To the left of face as displayed on webcam (Green)
        cv2.rectangle(_firstFrame, (x+(w/2),y+(2*h)), (x-(2*w), y+(4*h)), (0, 0,255), 2); #To the right of face as displayed on webcam

        roiGray = _grayFrame[y:y+(h/2), x:x+w];
        roiColor = _firstFrame[y:y+h, x:x+w];
        
        # show roi boxes
        #cv2.imshow("roiGray", roiGray);
        #cv2.imshow("roiColor", roiColor);

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = _eye_cascade.detectMultiScale(roiGray);
        for (ex,ey,ew,eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex+ew, ey+eh), (0,255,0), 1);

#TODO:  ESCAPE FUNCTION

def end():
    _originalFeed.release()
    cv2.destroyAllWindows()

#TODO:  MAIN FUNCTION

rval, frame = _originalFeed.read()

while rval:
    rval = firstFrame();

    _firstFrame = imutils.resize(_firstFrame, width=500);
    _grayFrame = cv2.cvtColor(_firstFrame, cv2.COLOR_BGR2GRAY);
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if _firstFrame is None:
        _firstFrame = _grayFrame;
        continue;

    #frameDelta = cv2.absdiff(_firstFrame, gray)
    #thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    #thresh = cv2.dilate(thresh, None, iterations=2)
    #(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #for c in cnts:
    #    if cv2.contourArea(c) < _args["min_area"]:
    #        continue
    #
    #    (mx, my, mw, mh) = cv2.boundingRect(c)
    #    cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (244, 66, 232), 2)
    
    faceDetect();
    
    updateFrameStatusTextOnFrame(_frameText);
    updateTimestampTextOnFrame();
    
    cv2.imshow("preview", _firstFrame);
    cv2.imshow("grayFeed", _grayFrame);

    key = cv2.waitKey(20);
    if key == 27:  # exit on ESC
        break;

end();
