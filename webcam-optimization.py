# This is going to be used to remove background images, to convert the color scheme of the video to grayscale, and to
# overall optimize the performance of our program

import cv2
import numpy

# cv2.namedWindow("Stream");
videoCapture = cv2.VideoCapture(0);

while True:
    ret, frame = videoCapture.read();
    grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    retr, threshold = cv2.threshold(grayScale, 110, 200, cv2.THRESH_BINARY);

#    cv2.imshow('frame', frame);
#    cv2.imshow('grayScale', grayScale);
    cv2.imshow('threshold', threshold);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;


videoCapture.release();
cv2.destroyAllWindows();