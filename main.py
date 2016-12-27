import numpy as np
import cv2
from eyeDetect import *

face_cascade = cv2.CascadeClassifier('./classifier/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./classifier/haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture('./data/7.mov')

face_location = []
eye_location = []

print "Hey"


while(cap.isOpened()):
    ret, img = cap.read() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # assume only one face in the video
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    true_face = []
    if len(faces) > 0:
        true_face = face_loacte(faces)
    if len(true_face) > 0:
        face_location = true_face
    if len(face_location) == 0:
        continue
    fx = face_location[0]
    fy = face_location[1]
    fw = face_location[2]
    fh = face_location[3]
    cv2.rectangle(img,(fx,fy),(fx+fw,fy+fh),(255,0,0),2)

    # crop the face window
    roi_gray = gray[fy:fy+fh, fx:fx+fw]
    roi_color = img[fy:fy+fh, fx:fx+fw]

    # find the eye location
    eyes = eye_cascade.detectMultiScale(roi_gray)
    true_eye = []
    if len(eyes) >= 2:
        true_eye = eye_locate(eyes)
    if len(true_eye) == 2:
        eye_location = true_eye
    if len(eye_location) == 0:
        continue
    e1_x = eye_location[0][0]
    e1_y = eye_location[0][1]
    e1_w = eye_location[0][2]
    e1_h = eye_location[0][3]
    e2_x = eye_location[1][0]
    e2_y = eye_location[1][1]
    e2_w = eye_location[1][2]
    e2_h = eye_location[1][3]
    cv2.rectangle(roi_color,(e1_x,e1_y),(e1_x+e1_w,e1_y+e1_h),(0,255,0),2)
    cv2.rectangle(roi_color,(e2_x,e2_y),(e2_x+e2_w,e2_y+e2_h),(0,255,0),2)

    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
