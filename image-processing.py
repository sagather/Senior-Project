import args as args
import cv2;
import argparse;
import datetime;
import imutils;
import time;

_faceCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml');
_eyeCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml');

def processImages(grayFeed):
    facesDetected = _faceCascade.detectMultiScale(grayFeed, 1.3, 5);

    #   For loop begin
    for (x, y, w, h) in facesDetected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2);
        roiGray = grayFeed[y:y + (h / 2), x:x + w];
        roiColor = frame[y:y + h, x:x + w];

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = _eyeCascade.detectMultiScale(roiGray);

        #   inner for loop begin
        for (ex, ey, ew, eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1);

        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)

        text = "Occupied"

        #inner for loop end

    #   Outer for loop end

    return roiColor;

def makeGrayscale(inputFrame):

    grayscale = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY);
    grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0);
    return grayscale;

def edgeDetection(grayScaleFrame):

    returnVal, edges = cv2.threshold(grayScaleFrame, 100, 200, cv2.THRESH_BINARY);
    return edges;


_videoCapture = cv2.VideoCapture(0);

ap = argparse.ArgumentParser();
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size");
args = vars(ap.parse_args());

#   While loop begin
while True:

    ret, frame = _videoCapture.read();
    text = "Neutral";
    grayscale = makeGrayscale(frame);

    if(firstframe is None):
        firstframe = grayscale;
        continue;

    frameDelta = cv2.absdiff(firstframe, grayscale);
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)



    cv2.imshow('face processed', processImages(grayscale));

    cv2.imshow('grayscale', grayscale);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

#   while loop end

_videoCapture.release();
cv2.destroyAllWindows();