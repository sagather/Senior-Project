import cv2 as cv
import numpy as np

class MotionDetectorContour:
    def __init__(self,ceil=15):
        self.ceil = ceil
        self.capture = cv.VideoCapture(0)
        # cv.imshow("Target", 1)

    def run(self):
        # Capture first frame to get size
        #self.capture.open()
        frame = self.capture.read()

        width = self.capture.get(3)
        height = self.capture.get(4)
        surface = width * height #Surface area of the image
        cursurface = 0 #Hold the current surface that have changed

        grey_image = np.zeros([int(height), int(width), 1], np.uint8)
        moving_average = np.zeros([int(height), int(width), 3], np.float32)
        difference = None

        while True:
            _, color_image = self.capture.read()
            color_image = cv.GaussianBlur(color_image, (21, 21), 0)

            if difference is None: #For the first time put values in difference, temp and moving_average
                difference = color_image.copy()
                temp = color_image.copy()
                cv.convertScaleAbs(color_image, moving_average, 1.0, 0.0)
            else:
                cv.accumulateWeighted(color_image, moving_average, 0.020, None) #Compute the average

            # Convert the scale of the moving average.
            cv.convertScaleAbs(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.absdiff(color_image, temp, difference)

            #Convert the image so that it can be thresholded
            cv.cvtColor(difference, cv.COLOR_RGB2GRAY, grey_image)
            cv.threshold(grey_image, 70, 255, cv.THRESH_BINARY, grey_image)
            kernel = np.ones((5, 5), np.uint8)


            cv.dilate(grey_image, kernel, 18) #to get object blobs
            # grey_image = cv.dilate(grey_image, kernel, 18)
            cv.erode(grey_image, kernel, 10)
            # grey_image = cv.erode(grey_image, kernel, 18)

            # Find contours

            image, contours, hierarchy = cv.findContours(grey_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = np.asarray(contours)
            backcontours = contours #Save contours

            for contour in contours: #For all contours compute the area
                cursurface += cv.contourArea(contour)
                #contours = contours.next()

            avg = (cursurface*100)/surface #Calculate the average of contour area on the total size
            if avg > self.ceil:
                print "Something is moving !"
            #print avg,"%"
            cursurface = 0 #Put back the current surface to 0

            #Draw the contours on the image
            _red =  (0, 0, 255); #Red for external contours
            _green =  (0, 255, 0);# Gren internal contours
            levels=1 #1 contours drawn, 2 internal contours as well, 3 ...
            cv.drawContours (color_image, backcontours, -1, (0, 255, 0), 2)

            cv.imshow("Target", color_image)

            # Listen for ESC or ENTER key
            c = cv.waitKey(7) % 0x100
            if c == 27 or c == 10:
                break


if __name__ == "__main__":
    t = MotionDetectorContour()
    t.run()