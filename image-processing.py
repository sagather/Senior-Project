# All import statements
import cv2
# for motion detection
import argparse
import datetime
import imutils
from Person import Person

# Referenced for motion detection:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# Might be needed later
#   _feedWidth = originalFeed.get(3)
#   _feedHeight = originalFeed.get(4)
#Global Variables

# _face_cascade = cv2.CascadeClassifier('HaarCascades\haarcascade_frontalface_default.xml')

# for James
_face_cascade = cv2.CascadeClassifier(
    '/Users/jamesbayman/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')

_originalFeed = cv2.VideoCapture(0)

_ap = argparse.ArgumentParser()
_ap.add_argument("-a", "--min-area", type=int, default=4000, help="minimum area size")
_args = vars(_ap.parse_args())

_firstFrame = None
_grayFrame = None
_frame = None
_thresh = None
_frameText = ""
_horizontal = None
_motionStateArray = [0, 0, 0, 0]
_people = []
_i = 0

def main():
    #global declarations
    global _firstFrame
    global _grayFrame
    global _frame
    global _motionStateArray
    global _thresh
    global _i

    #Content start
    rval = firstFrame()

    while rval:
        rval, _frame = _originalFeed.read()

        _frame = imutils.resize(_frame, width = 1000)
        _grayFrame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
        _grayFrame = cv2.GaussianBlur(_grayFrame, (21,21), 0)

        if _firstFrame is None:
            _firstFrame = _grayFrame
            continue

        frameDelta = cv2.absdiff(_firstFrame, _grayFrame)
        _thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        _thresh = cv2.dilate(_thresh, None, iterations=2)

        _motionStateArray = [0, 0, 0, 0]
        # List to hold people detected in frame
        _people = []
        # i to serve as an index when going through faces
        _i = 0
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
    global _people
    global _i
    global _

    #Content Start
    facesDectected = _face_cascade.detectMultiScale(_grayFrame, 1.3, 5)

    for (x, y, w, h) in facesDectected:
        # Add new person to people list if face detected
        _people.append(Person())
        currentPerson = _people[_i]

        # Lazy way to change color
        if _i == 0:
            Person.setColor(_people[_i], 255, 0, 0)  # Blue for 1st face
        if _i == 1:
            Person.setColor(_people[_i], 0, 255, 255)  # Yellow for 2nd face
        if _i == 2:
            Person.setColor(_people[_i], 255, 255, 0)  # Teal for 3rd face
        if _i == 3:
            Person.setColor(_people[_i], 0, 100, 255)  # Orange for 4th face

        cv2.rectangle(_frame, (x, y), (x + w, y + h),
                      (currentPerson.color[0], currentPerson.color[1], currentPerson.color[2]), 2)

        topLeft = [(x+w+w/2, y), (x+(3*w)+w, y+(2*h))]
        topRight = [(x-w/2, y), (x-(3*w), y+(2*h))]

        bottomLeft = [(x+w+w/2, y+(2*h)+(h/2)), (x+(3*w)+w, y+(5*h))]
        bottomRight = [(x-w/2, y+(2*h)+(h/2)), (x-(3*w), y+(5*h))]

        #top left
        cv2.rectangle(_frame, topLeft[0], topLeft[1], currentPerson.color, 2)
        #top right
        cv2.rectangle(_frame, topRight[0], topRight[1], currentPerson.color, 2)
        # bottom left
        cv2.rectangle(_frame, bottomLeft[0], bottomLeft[1], currentPerson.color, 2)
        # bottom right
        cv2.rectangle(_frame, bottomRight[0], bottomRight[1], currentPerson.color, 2)

        (_, cnts, _) = cv2.findContours(_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        _i += 1

        for c in cnts:
            if cv2.contourArea(c) < _args["min_area"]:
                continue

            (mx, my, mw, mh) = cv2.boundingRect(c)

            # coordinates for the smaller boxes
            smallx = mx + (mw / 4)
            smally = my + (mh / 4)
            smallw = mx + mw - (mw / 4)
            smallh = my + mh - (mh / 4)
            # midpoint of the box
            midx = mx + (mw / 2)
            midy = my + (my / 2)

            # rectangle must be in detection zones and smaller than detection area (I think)

            cv2.rectangle(_frame, (smallx, smally), (smallw, smallh), (244, 66, 232), 2)

            # Something Like this to check for specific motion?
            if (midx >= x - (2 * w) and midx <= x + (w / 2)) and (midy >= y and midy <= y + (2 * h)):
                _frameText = "                    Motion Top Right"
                _motionStateArray[1] = 1
            elif (midx <= x + (2 * w) + w) and (midx >= x + (w / 2)) and (midy >= y and midy <= y + (2 * h)):
                _frameText = "Motion Top Left"
                _motionStateArray[0] = 1
            elif (midx >= x - (2 * w) and midx <= x + (w / 2)) and (midy >= y + (2 * h) and midy <= y + (4 * h)):
                _frameText = "                    Motion Bottom Right"
                _motionStateArray[3] = 1
            elif (midx <= x + (2 * w) + w) and (midx >= x + (w / 2)) and (midy >= y + (2 * h) and midy <= y + (4 * h)):
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
    #cv2.imshow("grayFeed", _grayFrame);

def exitProcessing():
    global _originalFeed
    _originalFeed.release()
    cv2.destroyAllWindows()

def math():
    global _frameText
    global _motionStateArray
    #motion array needs to be revertedto zero if no motion is detected in the bounding boxes
    #check forward
    if _motionStateArray[0] == 1 and _motionStateArray[1] == 1:
        _frameText = "Forward"
    #check reverse
    elif _motionStateArray[2] == 1 and _motionStateArray[3] == 1:
        _frameText = "Reverse"
    #check forward left
    elif _motionStateArray[0] == 1:
        _frameText = "Forward Left"
    #check forward right
    elif _motionStateArray[1] == 1:
        _frameText = "Forward Right"
    #check reverse left
    elif _motionStateArray[2] == 1:
        _frameText = "Reverse Left"
    #check reverse right
    elif _motionStateArray[3] == 1:
        _frameText = "Reverse Right"
    else:
        _frameText = "Stop"


main()
exitProcessing()
