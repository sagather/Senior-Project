# All import statements
import cv2
# for motion detection
import argparse
import datetime
import imutils
from Person import Person
import Client

# Needs Refactoring
# Referenced for motion detection:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# Might be needed later
#   _feedWidth = originalFeed.get(3)
#   _feedHeight = originalFeed.get(4)
# Global Variables

_face_cascade = cv2.CascadeClassifier('HaarCascades\haarcascade_frontalface_default.xml')

# for Sam
# _face_cascade = cv2.CascadeClassifier(
# '/Users/bcxtr/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')

# for James
# _face_cascade = cv2.CascadeClassifier(
# '/Users/jamesbayman/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')

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
_people = []
_client = None


def main():
    # global declarations
    global _firstFrame
    global _grayFrame
    global _frame
    global _thresh
    global _people
    global _client

    # Content start
    rval = firstFrame()
    _client = Client

    while rval:
        rval, _frame = _originalFeed.read()

        _frame = imutils.resize(_frame, width=1000)
        _grayFrame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
        _grayFrame = cv2.GaussianBlur(_grayFrame, (21, 21), 0)

        if _firstFrame is None:
            _firstFrame = _grayFrame
            continue

        frameDelta = cv2.absdiff(_firstFrame, _grayFrame)
        _thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        _thresh = cv2.dilate(_thresh, None, iterations=2)

        # List to hold people detected in frame

        # i to serve as an index when going through faces
        faceDetection()
        math()
        displayProcessing()

        for peeps in _people:
            peeps.clearMotion()

        del _people[:]

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break


def firstFrame():
    global _frame
    global _frameText
    global _originalFeed
    if _originalFeed.isOpened():  # try to get the first frame
        rvalLocal, _frame = _originalFeed.read()
        _frameText = "stop"
        _client.send("stop")
        return rvalLocal


def faceDetection():
    # global declarations
    global _firstFrame
    global _frameText
    global _frame
    global _face_cascade
    global _thresh
    global _frameText
    global _horizontal
    global _people

    # Content Start
    _i = 0
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

        topLeft = [(x + w + w / 2, y), (x + (3 * w) + w, y + (2 * h))]
        topRight = [(x - w / 2, y), (x - (3 * w), y + (2 * h))]

        bottomLeft = [(x + w + w / 2, y + (2 * h) + (h / 2)), (x + (3 * w) + w, y + (5 * h))]
        bottomRight = [(x - w / 2, y + (2 * h) + (h / 2)), (x - (3 * w), y + (5 * h))]

        # top left
        cv2.rectangle(_frame, topLeft[0], topLeft[1], currentPerson.color, 2)
        # top right
        cv2.rectangle(_frame, topRight[0], topRight[1], currentPerson.color, 2)
        # bottom left
        cv2.rectangle(_frame, bottomLeft[0], bottomLeft[1], currentPerson.color, 2)
        # bottom right
        cv2.rectangle(_frame, bottomRight[0], bottomRight[1], currentPerson.color, 2)

        (_, cnts, _) = cv2.findContours(_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) < _args["min_area"]:
                continue

            (mx, my, mw, mh) = cv2.boundingRect(c)

            # coordinates for the smaller boxes
            # top left corner
            smallx = mx + (mw / 4)
            smally = my + (mh / 4)
            # bottom right corner
            smalla = mx + mw - (mw / 4)
            smallb = my + mh - (mh / 4)
            # width and height
            smallw = mw - (mw / 4)
            smallh = mh - (mh / 4)

            # midpoint of the box (not actually right now, im gonna fix it)
            midx = smallx + (smallw / 2)
            midy = smally + (smallh / 2)

            # rectangle must be in detection zones and smaller than detection area (I think)

            if inBounds(smallx, smally, smallw, smallh, x, y, w, h):
                cv2.rectangle(_frame, (smallx, smally), (smalla, smallb), (244, 66, 232), 2)
                if topRightBound(smallx, smally, smallw, smallh, x, y, w, h):
                    Person.setMotion(_people[_i], 1, 1)
                elif topLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
                    Person.setMotion(_people[_i], 0, 1)
                elif bottomRightBound(smallx, smally, smallw, smallh, x, y, w, h):
                    Person.setMotion(_people[_i], 3, 1)
                elif bottomLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
                    Person.setMotion(_people[_i], 2, 1)
        _i += 1


def displayProcessing():
    global _horizontal
    global _frame
    global _grayFrame
    global _frameText
    global _people

    _horizontal = cv2.flip(_frame, 1)
    cv2.putText(_horizontal, "Frame Status: {}".format(_frameText), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(_horizontal, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, _frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.putText(_horizontal, "Faces in frame: {}".format(len(_people)), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    _client.send(_frameText)

    # if not _horizontal.data:
    cv2.imshow("preview", _horizontal)
    # cv2.imshow("grayFeed", _grayFrame);


def exitProcessing():
    global _originalFeed
    _originalFeed.release()
    cv2.destroyAllWindows()


def math():
    global _frameText
    global _people
    masterMotionStateArray = [0, 0, 0, 0]

    numPeople = len(_people)
    divideby = 0

    if numPeople == 4:
        divideby = 3
    elif numPeople == 3:
        divideby = 2
    elif numPeople == 0:
        divideby = 100
    else:
        divideby = numPeople

    for peeps in _people:
        print(peeps.motion)
        # motion array needs to be reverted to zero if no motion is detected in the bounding boxes
        if peeps.motion[0] == 1 and peeps.motion[1] == 1:
            masterMotionStateArray[0] = masterMotionStateArray[0] + 1
            masterMotionStateArray[1] = masterMotionStateArray[1] + 1
        elif peeps.motion[2] == 1 and peeps.motion[3] == 1:
            masterMotionStateArray[2] = masterMotionStateArray[2] + 1
            masterMotionStateArray[3] = masterMotionStateArray[3] + 1
        elif peeps.motion[0] == 1:
            masterMotionStateArray[0] = masterMotionStateArray[0] + 1
        elif peeps.motion[1] == 1:
            masterMotionStateArray[1] = masterMotionStateArray[1] + 1
        elif peeps.motion[2] == 1:
            masterMotionStateArray[2] = masterMotionStateArray[2] + 1
        elif peeps.motion[3] == 1:
            masterMotionStateArray[3] = masterMotionStateArray[3] + 1

    # check forward
    if masterMotionStateArray[0] >= divideby and masterMotionStateArray[1] >= divideby:
        _frameText = "forward"
    # check reverse
    elif masterMotionStateArray[2] >= divideby and masterMotionStateArray[3] >= divideby:
        _frameText = "reverse"
    # check forward left
    elif masterMotionStateArray[0] >= divideby:
        _frameText = "left"
    # check forward right
    elif masterMotionStateArray[1] >= divideby:
        _frameText = "right"
    # check reverse left
    elif masterMotionStateArray[2] >= divideby:
        _frameText = "reverse"
    # check reverse right
    elif masterMotionStateArray[3] >= divideby:
        _frameText = "reverse"
    else:
        _frameText = "stop"


def inBounds(smallx, smally, smallw, smallh, x, y, w, h):
    if topLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
        return True
    elif topRightBound(smallx, smally, smallw, smallh, x, y, w, h):
        return True
    elif bottomLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
        return True
    elif bottomRightBound(smallx, smally, smallw, smallh, x, y, w, h):
        return True
    else:
        return False


def topLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
    if smallx > x+w+w/2 and smallx + smallw <= x+(3*w)+w:
        if (smally > y and smally + smallh < y+(2*h)):
            return True
    else:
        return False

def topRightBound(smallx, smally, smallw, smallh, x, y, w, h):
    if smallx + smallw < (x-w/2) and smallx > x-(3*w):
        if smally > y and smally + smallh < (y+(2*h)):
            return True
    else:
        return False

def bottomLeftBound(smallx, smally, smallw, smallh, x, y, w, h):
    if smallx > x+w+w/2 and smallx + smallw < (x+(3*w)+w):
        if smally > y+(2*h)+(h/2) and smally + smallh < (y+(5*h)):
            return True
    else:
        return False

def bottomRightBound(smallx, smally, smallw, smallh, x, y, w, h):
    if smallx + smallw < (x-w/2) and smallx > x-(3*w):
        if smally > y+(2*h)+(h/2) and smally + smallh < (y+(5*h)):
            return True
    else:
        return False


main()
exitProcessing()
