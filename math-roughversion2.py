# All import statements
import cv2
# for motion detection
import argparse
import datetime
import imutils
from Person import Person
import numpy as np
#import Client

# Needs Refactoring
# Referenced for motion detection:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

_face_cascade = cv2.CascadeClassifier('HaarCascades\haarcascade_frontalface_default.xml')

# for Sam
# _face_cascade = cv2.CascadeClassifier(
# '/Users/bcxtr/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')

# for James
# _face_cascade = cv2.CascadeClassifier(_originalFeed = cv2.VideoCapture(0)
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
_width = None
_height = None
_surface = None
_cursurface = 0
_difference =None
_temp = None
_grey_image = None
_moving_average = None
#_client = None


def main():
    # global declarations
    global _firstFrame
    global _grayFrame
    global _frame
    global _thresh
    global _people
    global _difference
    global _grey_image
    global _moving_average
    #global _client

    # Content start
    rval = firstFrame()
    #_client = Client

    _width = _originalFeed.get(3)
    _height = _originalFeed.get(4)
    _surface = _width * _height
    _cursurface = 0
    _difference = None
    _grey_image = np.zeros([int(_height), int(_width), 1], np.uint8)
    _moving_average = np.zeros([int(_height), int(_width), 3], np.float32)

    while rval:
        rval, _frame = _originalFeed.read()
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
        #_client.send("stop")
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
    global _originalFeed


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
        motionDetection(x, y, w, h, _i)



def motionDetection(x, y, w, h, _i):
    global _width
    global _height
    global _people
    global _originalFeed
    global _frame
    global _cursurface
    global _surface
    global _difference
    global _temp
    global _grey_image
    global _moving_average

    _, color_image = _originalFeed.read()
    #color_copy = color_image.copy()
    color_image = cv2.GaussianBlur(color_image, (21, 21), 0)
    if _difference is None:
        _difference = color_image.copy()
        _temp = color_image.copy()
        cv2.convertScaleAbs(color_image, _moving_average, 1, 0.0)
    else:
        cv2.accumulateWeighted(color_image, _moving_average, 0.020, None)

    cv2.convertScaleAbs(_moving_average, _temp, 1.0, 0.0)

    cv2.absdiff(color_image, _temp, _difference)

    cv2.cvtColor(_difference, cv2.COLOR_RGB2GRAY, _grey_image)
    cv2.threshold(_grey_image, 70, 255, cv2.THRESH_BINARY, _grey_image)
    kernel = np.ones((5, 5), np.uint8)

    cv2.dilate(_grey_image, kernel, 18)
    cv2.erode(_grey_image, kernel, 10)

    contours = cv2.findContours(_grey_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    backcontours = contours  # Save contours

    for contour in contours:  # For all contours compute the area and get center point
        _cursurface += cv2.contourArea(contour)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

    # draw contour and midpoint circle
        if inBounds(x, y, w, h, cX, cY):
            cv2.drawContours(_frame, [contour], -2, (0, 255, 0), 2)
            cv2.circle(_frame, (cX, cY), 3, (255, 0, 0), -1)
            if topRightBound(x, y, w, h, cX, cY):
                Person.setMotion(_people[_i], 1, 1)
            elif topLeftBound(x, y, w, h, cX, cY):
                Person.setMotion(_people[_i], 0, 1)
            elif bottomRightBound(x, y, w, h, cX, cY):
                Person.setMotion(_people[_i], 3, 1)
            elif bottomLeftBound(x, y, w, h, cX, cY):
                Person.setMotion(_people[_i], 2, 1)



def displayProcessing():
    global _horizontal
    global _frame
    global _grayFrame
    global _frameText
    global _people
    global _difference

    _horizontal = cv2.flip(_frame, 1)
    _horizontal = imutils.resize(_horizontal, width=1000)
    cv2.putText(_horizontal, "Frame Status: {}".format(_frameText), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(_horizontal, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, _horizontal.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.putText(_horizontal, "Faces in frame: {}".format(len(_people)), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #_client.send(_frameText)

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


def inBounds(x, y, w, h, cX, cY):
    if topLeftBound(x, y, w, h, cX, cY):
        return True
    elif topRightBound(x, y, w, h, cX, cY):
        return True
    elif bottomLeftBound(x, y, w, h, cX, cY):
        return True
    elif bottomRightBound(x, y, w, h, cX, cY):
        return True
    else:
        return False


def topLeftBound(x, y, w, h, cX, cY):
    if cX > x+w+w/2 and cX  <= x+(3*w)+w:
        if (cY > y and cY < y+(2*h)):
            return True
    else:
        return False

def topRightBound(x, y, w, h, cX, cY):
    if cX < (x-w/2) and cX > x-(3*w):
        if cY > y and cY < (y+(2*h)):
            return True
    else:
        return False

def bottomLeftBound(x, y, w, h, cX, cY):
    if cX > x+w+w/2 and cX < (x+(3*w)+w):
        if cY > y+(2*h)+(h/2) and cY < (y+(5*h)):
            return True
    else:
        return False

def bottomRightBound(x, y, w, h, cX, cY):
    if cX < (x-w/2) and cX > x-(3*w):
        if cY > y+(2*h)+(h/2) and cY < (y+(5*h)):
            return True
    else:
        return False


main()
exitProcessing()
