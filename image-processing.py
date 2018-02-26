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

#Global Variables
_face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')

_originalFeed = cv2.VideoCapture(0)

_ap = argparse.ArgumentParser()
_ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
_args = vars(_ap.parse_args())

_firstFrame = None
_grayFrame = None
_frame = None
_thresh = None
_frameText = ""
_horizontal = None
_motionStateArray = [0, 0, 0, 0]

def main():
    #global declarations
    global _firstFrame
    global _grayFrame
    global _frame
    global _motionStateArray
    global _thresh

    #Content start
    rval = firstFrame()

    while rval:
        rval, _frame = _originalFeed.read()

        _frame = imutils.resize(_frame, width = 500)
        _grayFrame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
        _grayFrame = cv2.GaussianBlur(_grayFrame, (21,21), 0)

        if _firstFrame is None:
            _firstFrame = _grayFrame
            continue

        frameDelta = cv2.absdiff(_firstFrame, _grayFrame)
        _thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        _thresh = cv2.dilate(_thresh, None, iterations=2)

        _motionStateArray = [0, 0, 0, 0]
        faceDetection()
        displayProcessing()

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break


def firstFrame():
    global _frame
    global _frameText
    global _originalFeed
    if _originalFeed.isOpened():  # try to get the first frame
        rvalLocal, _frame = _originalFeed.read()
        _frameText = "No Motion"
        return rvalLocal

def faceDetection():
    #global declarations
    global _firstFrame
    global _frameText
    global _frame
    global _face_cascade
    global _thresh
    global _frameText
    global _motionStateArray
    global _horizontal

    #Content Start
    facesDectected = _face_cascade.detectMultiScale(_grayFrame, 1.3, 5)

    for (x, y, w, h) in facesDectected:
        cv2.rectangle(_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Top
        # To the left of face as displayed on  (Green)
        cv2.rectangle(_frame, (x+(w/2), y), (x-(2*w), y+(2*h)), (0, 255, 0), 2)
        # To the right of face as displayed on webcam (Red)
        cv2.rectangle(_frame, (x+(w/2), y), (x+(2*w)+w, y+(2*h)), (0, 0, 255), 2)
        # Bottom
        # To the left of face as displayed on webcam (Green)
        cv2.rectangle(_frame, (x+(w/2), y+(2*h)), (x+(2*w)+w, y+(4*h)), (0, 255, 0), 2)
        # To the right of face as displayed on webcam
        cv2.rectangle(_frame, (x+(w/2), y+(2*h)), (x-(2*w), y+(4*h)), (0, 0, 255), 2)

        (_, cnts, _) = cv2.findContours(_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) < _args["min_area"]:
                continue

            (mx, my, mw, mh) = cv2.boundingRect(c)
            cv2.rectangle(_frame, (mx, my), (mx + mw, my + mh), (244, 66, 232), 2)

            # Something Like this to check for specific motion?
            if (mx >= x-(2*w) and mx <= x+(w/2)) and (my >= y and my <= y+(2*h)):
                _frameText = "                    Motion Top Right"
                _motionStateArray[1] = 1
            elif (mx <= x+(2*w)+w) and (mx >= x+(w/2)) and (my >= y and my <= y+(2*h)):
                _frameText = "Motion Top Left"
                _motionStateArray[0] = 1
            elif (mx >= x-(2*w) and mx <= x+(w/2)) and (my >= y + (2 * h) and my <= y + (4 * h)):
                _frameText = "                    Motion Bottom Right"
                _motionStateArray[3] = 1
            elif (mx <= x+(2*w)+w) and (mx >= x+(w/2)) and (my >= y+(2*h) and my <= y+(4*h)):
                _frameText = "Motion Bottom Left"
                _motionStateArray[2] = 1

            if _motionStateArray[0] == 1 and _motionStateArray[1] == 1:
                _frameText = "    Motion BOTH Top"
            if _motionStateArray[2] == 1 and _motionStateArray[3] == 1:
                _frameText = "    Motion BOTH Bottom"

def displayProcessing():
    global _horizontal
    global _frame
    global _grayFrame
    global _frameText

    _horizontal = cv2.flip(_frame, 1)
    cv2.putText(_horizontal, "Frame Status: {}".format(_frameText), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(_horizontal, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, _frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #if not _horizontal.data:
    cv2.imshow("preview", _horizontal)
    cv2.imshow("grayFeed", _grayFrame);

def exitProcessing():
    global _originalFeed
    _originalFeed.release()
    cv2.destroyAllWindows()


main()
exitProcessing()
