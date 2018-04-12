import cv2
import numpy as np
import imutils

capture = cv2.VideoCapture(0)

frame = capture.read()

width = capture.get(3)
height = capture.get(4)

surface = width * height #Surface area of the image

cursurface = 0 #Hold the current surface that have changed

######
grey_image = cv2.convertScaleAbs()
moving_average = np.zeros((int(width), int(height)), np.uint32, 3)

#grey_image = np.zeros((int(width), int(height)), np.uint8, 1)
#moving_average = np.zeros((int(width), int(height)), np.uint32, 3)
######

difference = None

while True:
    _, color_image = capture.read()
    color_image = cv2.GaussianBlur(color_image, (21, 21), 0)

########################
    if not difference: #For the first time put values in difference, temp and moving_average
        difference = color_image.copy()
        temp = color_image.copy()
        cv2.convertScaleAbs(color_image, moving_average, 1.0, 0.0)
    else:
        cv2.runningAvg(color_image, moving_average, 0.020, None) #Compute the average

    # Convert the scale of the moving average.
    cv2.convertScale(moving_average, temp, 1.0, 0.0)

    # Minus the current frame from the moving average.
    cv2.absDiff(color_image, temp, difference)

    #Convert the image so that it can be thresholded
    cv2.cvtColor(difference, grey_image, cv2.COLOR_RGB2GRAY)
    cv2.threshold(grey_image, grey_image, 70, 255, cv2.THRESH_BINARY)

    cv2.dilate(grey_image, grey_image, None, 18) #to get object blobs
    cv2.erode(grey_image, grey_image, None, 10)

    # Find contours
    storage = cv2.createMemStorage(0)
    contours = cv2.findContours(grey_image, storage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    backcontours = contours #Save contours

    while contours: #For all contours compute the area
        cursurface += cv2.contourArea(contours)
        contours = contours.h_next()

    avg = (cursurface*100)/surface #Calculate the average of contour area on the total size
    if avg > self.ceil:
        print "Something is moving !"
    #print avg,"%"
    cursurface = 0 #Put back the current surface to 0

    #Draw the contours on the image
    _red =  (0, 0, 255); #Red for external contours
    _green =  (0, 255, 0);# Gren internal contours
    levels=1 #1 contours drawn, 2 internal contours as well, 3 ...
    cv2.drawContours (color_image, backcontours,  _red, _green, levels, 2, cv2.CV_FILLED)

    cv2.imshow("Target", color_image)


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