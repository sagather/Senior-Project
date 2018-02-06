
#Tester for fullbody tracking using haar cascades and openCV

import cv2
import numpy

#fullBodyCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_fullbody.xml')

#lowerBodyCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_lowerbody.xml')

upperBodyCascade = cv2.CascadeClassifier('HaarCascades/haarcascade_upperbody.xml')

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

while True:
    ret, img = vc.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    body = upperBodyCascade.detectMultiScale(gray)
    for (x, y, w, h) in body:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    cv2.imshow('preview',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
vc.release()
cv2.destroyAllWindows()