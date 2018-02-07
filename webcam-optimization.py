# This is going to be used to remove background images, to convert the color scheme of the video to grayscale, and to
# overall optimize the performance of our program

import cv2
import numpy

# cv2.namedWindow("Stream");
videoCapture = cv2.VideoCapture(0);

while True:
    ret, frame = videoCapture.read();
    grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    retr, threshold = cv2.threshold(grayScale, 100, 200, cv2.THRESH_BINARY);

    laplacian = cv2.Laplacian(threshold, cv2.CV_64F);

    #   the edges one is less reliable, albeit, might make our job to recognize things easier
    edges = cv2.Canny(grayScale, 100, 200);
#    sobelx = cv2.Sobel(threshold, cv2.CV_64F, 1, 0, ksize=5);
#    sobely = cv2.Sobel(threshold, cv2.CV_64F, 0, 1, ksize=5);

#    cv2.imshow('frame', frame);
#    cv2.imshow('grayScale', grayScale);
    cv2.imshow('threshold', threshold);
    cv2.imshow('laplacian', laplacian);
    #   I really don't like the edges one as much.  It losees track of things pretty quickly
    cv2.imshow('edges', edges);
#    cv2.imshow('sobelx', sobelx);
#    cv2.imshow('sobely', sobely);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;


videoCapture.release();
cv2.destroyAllWindows();