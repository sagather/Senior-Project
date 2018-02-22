# All import statements

import cv2
# for motion detection
import argparse
import datetime
import imutils

# Referenced for motion detection:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# Might be needed later
#   _feedWidth = originalFeed.get(3)
#   _feedHeight = originalFeed.get(4)

# Load in cascade files
_face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
_eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')

_originalFeed = cv2.VideoCapture(0)

_ap = argparse.ArgumentParser()
_ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
_args = vars(_ap.parse_args())

_firstFrame = None
_grayFrame = None
_frameText = ""


def firstFrame():
    global _firstFrame
    global _frameText
    if _originalFeed.isOpened():  # try to get the first frame
        rvalLocal, _firstFrame = _originalFeed.read()
        _frameText = "No Motion"
        return rvalLocal


def updateFrameStatusTextOnFrame(statusStr):
    cv2.putText(_firstFrame, "Frame Status: {}".format(statusStr), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def updateTimestampTextOnFrame():
    cv2.putText(_firstFrame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, _firstFrame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


def faceDetect():
    facesDetected = _face_cascade.detectMultiScale(_grayFrame, 1.3, 5)
    for (x, y, w, h) in facesDetected:
        cv2.rectangle(_firstFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Top
        # To the left of face as displayed on  (Green)
        cv2.rectangle(_firstFrame, (x+(w/2), y), (x-(2*w), y+(2*h)), (0, 255, 0), 2)
        # To the right of face as displayed on webcam (Red)
        cv2.rectangle(_firstFrame, (x+(w/2), y), (x+(2*w)+w, y+(2*h)), (0, 0, 255), 2)
        # Bottom
        # To the left of face as displayed on webcam (Green)
        cv2.rectangle(_firstFrame, (x+(w/2), y+(2*h)), (x+(2*w)+w, y+(4*h)), (0, 255, 0), 2)
        # To the right of face as displayed on webcam
        cv2.rectangle(_firstFrame, (x+(w/2), y+(2*h)), (x-(2*w), y+(4*h)), (0, 0, 255), 2)

        # setup roi boxes
        roiGray = _grayFrame[y:y+(h/2), x:x+w]
        roiColor = _firstFrame[y:y+h, x:x+w]

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = _eye_cascade.detectMultiScale(roiGray)
        for (ex, ey, ew, eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 1)


def end():
    _originalFeed.release()
    cv2.destroyAllWindows()


# MAIN FUNCTION
rval = True

while rval:
    rval = firstFrame()

    if _firstFrame is None:
        print("Error: _firstFrame was not set")
        break

    _firstFrame = imutils.resize(_firstFrame, width=500)
    _grayFrame = cv2.cvtColor(_firstFrame, cv2.COLOR_BGR2GRAY)

    faceDetect()
    
    updateFrameStatusTextOnFrame(_frameText)
    updateTimestampTextOnFrame()
    
    cv2.imshow("preview", _firstFrame)

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

end()
