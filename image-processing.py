import cv2

_faceCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
_eyeCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')

def processImages(grayFeed):
    facesDetected = _faceCascade.detectMultiScale(grayFeed, 1.3, 5)
    for (x, y, w, h) in facesDetected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roiGray = grayFeed[y:y + (h / 2), x:x + w]
        roiColor = frame[y:y + h, x:x + w]

        # Detect eyes using haarcascade_eye.xml
        eyesDetected = _eyeCascade.detectMultiScale(roiGray)
        for (ex, ey, ew, eh) in eyesDetected:
            cv2.rectangle(roiColor, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
    return roiColor;

def makeGrayscale(inputFrame):

    grayscale = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY);
    return grayscale;

def edgeDetection(grayScaleFrame):

    returnVal, edges = cv2.threshold(grayScaleFrame, 100, 200, cv2.THRESH_BINARY);
    return edges;


_videoCapture = cv2.VideoCapture(0);

while True:

    ret, frame = _videoCapture.read();
    grayscale = makeGrayscale(frame);

    cv2.imshow('face processed', processImages(grayscale));

    cv2.imshow('grayscale', grayscale);



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;


_videoCapture.release();
cv2.destroyAllWindows();