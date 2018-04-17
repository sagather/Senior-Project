# Refactored Code
# Imports
import cv2
import numpy as np
import argparse
import datetime
import imutils
from Person import Person
import Client

# References for Motion Detection:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# http://www.robindavid.fr/opencv-tutorial/motion-detection-with-opencv.html

# Sam
# face_cascade = cv2.CascadeClassifier(
# '/Users/bcxtr/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')


# James
# face_cascade = cv2.CascadeClassifier(
# '/Users/jamesbayman/PycharmProjects/Senior-Project/HaarCascades/haarcascade_frontalface_default.xml')

# The Haar Cascade for Face Detection - An Open Source Resource
_face_cascade = cv2.CascadeClassifier('HaarCascades\haarcascade_frontalface_default.xml')

# The starter video feed
_originalFeed = cv2.VideoCapture(0)

# Global Variables
_firstFrame = None
_grayFrame = None
_frame = None
_thresh = None
_frameText = ""
_horizontal = None
_people = []
_width = None
_height = None
_cur_surface = 0
_difference =None
_temp = None
_grey_image = None
_moving_average = None
_client = None

def main():
    # Global Declarations
    global _firstFrame
    global _grayFrame
    global _frame
    global _thresh
    global _people
    global _difference
    global _grey_image
    global _moving_average
    global _width
    global _height
    global _client

    # Main Code
    rval = firstFrame()
    _client = Client()
    _width = _originalFeed.get(3)
    _height = _originalFeed.get(4)
    _grey_image = np.zeros([int(_height), int(_width), 1], np.uint8)
    _moving_average = np.zeros([int(_height), int(_width), 3], np.float32)

    while rval:
        rval, _frame = _originalFeed.read()
        _grayFrame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
        _grayFrame = cv2.GaussianBlur(_grayFrame, (21, 21), 0)

        # Check if the initial frame is empty
        if _firstFrame is None:
            _firstFrame = _grayFrame
            continue

        # Get the thresh of the frame for easier detection
        frameDelta = cv2.absdiff(_firstFrame, _grayFrame)
        _thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        _thresh = cv2.dilate(_thresh, None, iterations=2)

        # Calls to other methods
        faceDetection()
        math()
        displayProcessing()

        # Empty the motion array of people for a clean starting point for the next iteration
        for people in _people:
            people.clearMotion()

        # Empty the contents of the people array
        del _people[:]

        # Check if escape is pressed to close the program
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break


def firstFrame():
    # Global Declarations
    global _frame
    global _frameText
    global _originalFeed

    # Content Start
    # Try to get the first frame
    if _originalFeed.isOpened():
        rvalLocal, _frame = _originalFeed.read()
        _frameText = "stop"
        _client.send("stop")
        return rvalLocal


def faceDetection():
    # Global Declarations
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
    # Iterate through all the detected faces
    for (x, y, w, h) in facesDectected:
        # Add new person to people list if face detected
        _people.append(Person())

        # get a color for the persons face detection
        getColor(_i)

        # Draw the initial face box
        cv2.rectangle(_frame, (x, y), (x + w, y + h),
                      (_people[_i].color[0], _people[_i].color[1], _people[_i].color[2]), 2)

        # Bounding box locations
        topLeft = [(x + w, y), (x + int(round(2.5 * w)), y + int(round(1.5 * h)))]
        topRight = [(x, y), (x - int(round(1.5 * w)), y + int(round(1.5 * h)))]

        bottomLeft = [(x + int(round(1.5*w)), y + int(round(2.5 * h)) + (h / 2)), (x + (2 * w) + w, y + int(round(5.5 * h)))]
        bottomRight = [(x - int(round(w/2)), y + int(round(2.5 * h)) + (h / 2)), (x - (2 * w), y + int(round(5.5 * h)))]

        # Draw bounding boxes
        # top left
        cv2.rectangle(_frame, topLeft[0], topLeft[1], _people[_i].color, 2)
        # top right
        cv2.rectangle(_frame, topRight[0], topRight[1], _people[_i].color, 2)
        # bottom left
        cv2.rectangle(_frame, bottomLeft[0], bottomLeft[1], _people[_i].color, 2)
        # bottom right
        cv2.rectangle(_frame, bottomRight[0], bottomRight[1], _people[_i].color, 2)

        # Call on the motion detection only if a face is detected
        print("x: {} y: {} w: {} h: {} i:{}".format(x,y,w,h,_i))
        motionDetection(x, y, w, h, _i)
        _i = _i + 1




def motionDetection(x, y, w, h, _i):
    # Global Dec
    global _width
    global _height
    global _people
    global _originalFeed
    global _frame
    global _cur_surface
    global _difference
    global _temp
    global _grey_image
    global _moving_average

    # Content Start
    _, color_image = _originalFeed.read()
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
    temp = [0, 0, 0, 0]
    for contour in contours:  # For all contours compute the area and get center point
        _cur_surface += cv2.contourArea(contour)
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
                temp[1] = 1
            elif topLeftBound(x, y, w, h, cX, cY):
                temp[0] = 1
            elif bottomRightBound(x, y, w, h, cX, cY):
                temp[3] = 1
            elif bottomLeftBound(x, y, w, h, cX, cY):
                temp[2] = 1
    Person.setMotion(_people[_i],temp[0], temp[1], temp[2], temp[3])


def displayProcessing():
    # Global Declarations
    global _horizontal
    global _frame
    global _grayFrame
    global _frameText
    global _people
    global _difference

    # Content Start
    _horizontal = cv2.flip(_frame, 1)
    _horizontal = imutils.resize(_horizontal, width=1000)
    cv2.putText(_horizontal, "Frame Status: {}".format(_frameText), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(_horizontal, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, _horizontal.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.putText(_horizontal, "Faces in frame: {}".format(len(_people)), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    _client.send(_frameText)

    cv2.imshow("preview", _horizontal)


def math():
    # Global Declarations
    global _frameText
    global _people
    
    # Content Start
    masterMotionStateArray = [0, 0, 0, 0]
    numPeople = len(_people)
    if numPeople == 1 or numPeople == 2:
        divideby = numPeople
    elif numPeople > 2:
        divideby = round(numPeople/2)
    else:
        divideby = 100000;

    for people in _people:
        if people.motion[0] == 1 and people.motion[1] == 1:
            masterMotionStateArray[0] = masterMotionStateArray[0] + 1
            masterMotionStateArray[1] = masterMotionStateArray[1] + 1
        elif people.motion[2] == 1 and people.motion[3] == 1:
            masterMotionStateArray[2] = masterMotionStateArray[2] + 1
            masterMotionStateArray[3] = masterMotionStateArray[3] + 1
        elif people.motion[0] == 1:
            masterMotionStateArray[0] = masterMotionStateArray[0] + 1
        elif people.motion[1] == 1:
            masterMotionStateArray[1] = masterMotionStateArray[1] + 1
        elif people.motion[2] == 1:
            masterMotionStateArray[2] = masterMotionStateArray[2] + 1
        elif people.motion[3] == 1:
            masterMotionStateArray[3] = masterMotionStateArray[3] + 1
        people.clearMotion

    # default
    if numPeople == 0:
        _frameText = "stop"
    # check forward
    if masterMotionStateArray[0] == masterMotionStateArray[1] and masterMotionStateArray[0] >= divideby and masterMotionStateArray[1] >= divideby:
        _frameText = "forward"
    # check reverse
    elif masterMotionStateArray[2] == masterMotionStateArray[3] and masterMotionStateArray[2] >= divideby and masterMotionStateArray[3] >= divideby:
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
    # Content Start
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


# topLeft = [(x + w, y), (x + int(round(2.5 * w)), y + int(round(1.5 * h)))]
def topLeftBound(x, y, w, h, cX, cY):
    topLeft = [(x + w), y, x + int(round(2.5 * w)), y + int(round(1.5 * h))]
    if cX > topLeft[0] and cX  <= topLeft[2]:
        if cY > topLeft[1] and cY < topLeft[3]:
            return True
    else:
        return False


# topRight = [(x, y), (x - int(round(1.5 * w)), y + int(round(1.5 * h)))]
def topRightBound(x, y, w, h, cX, cY):
    topRight = [x, y, x - int(round(1.5 * w)), y + int(round(1.5 * h))]
    if cX < topRight[0] and cX > topRight[2]:
        if cY > topRight[1] and cY < topRight[3]:
            return True
    else:
        return False


# bottomLeft = [(x + int(round(1.5*w)), y + int(round(2.5 * h)) + (h / 2)), (x + (2 * w) + w, y + int(round(5.5 * h)))]
def bottomLeftBound(x, y, w, h, cX, cY):
    bottomLeft = [x + int(round(1.5*w)), y + int(round(2.5 * h) + (h / 2)), x + (2 * w) + w, y + int(round(5.5 * h))]
    if cX > bottomLeft[0] and cX < bottomLeft[2]:
        if cY > bottomLeft[1] and cY < bottomLeft[3]:
            return True
    else:
        return False


# bottomRight = [(x - int(round(w/2)), y + int(round(2.5 * h)) + (h / 2)), (x - (2 * w), y + int(round(5.5 * h)))]
def bottomRightBound(x, y, w, h, cX, cY):
    bottomRight = [x - int(round(w/2)), y + int(round(2.5 * h) + (h / 2)), x - (2 * w), y + int(round(5.5 * h))]
    if cX < bottomRight[0] and cX > bottomRight[2]:
        if cY > bottomRight[1] and cY < bottomRight[3]:
            return True
    else:
        return False

# Generic color creator for the face boxes, defaults to black if there are more than 8 people
def getColor(_i):
    # Global Declarations
    global _people
    # Content Start
    if _i == 0:
        Person.setColor(_people[_i], 255, 0, 0)  # Blue for 1st face
    elif _i == 1:
        Person.setColor(_people[_i], 0, 255, 255)  # Yellow for 2nd face
    elif _i == 2:
        Person.setColor(_people[_i], 255, 255, 0)  # Teal for 3rd face
    elif _i == 3:
        Person.setColor(_people[_i], 0, 100, 255)  # Orange
    elif _i == 4:
        Person.setColor(_people[_i], 255, 0, 255)  # Purple
    elif _i == 5:
        Person.setColor(_people[_i], 255, 255, 255)  # White
    elif _i == 6:
        Person.setColor(_people[_i], 100, 100, 100)  # Grey
    elif _i == 7:
        Person.setColor(_people[_i], 140, 0, 255)  # Pink
    else:
        Person.setColor(_people[_i], 0, 0, 0)  # Black


def exitProcessing():
    # Global Declarations
    global _originalFeed
    # Content Start
    _originalFeed.release()
    cv2.destroyAllWindows()


main()
exitProcessing()
