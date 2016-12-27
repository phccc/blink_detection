import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('./classifier/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./classifier/haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture('./data/2.mov')

test_arr = []

test_num = 0
test_limit = 300

while(cap.isOpened()):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        if len(eyes) > 1:
        	test_arr.append(eyes[0])
        	test_arr.append(eyes[1])

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


    test_num = test_num + 1
    if test_num > test_limit:
    	break
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print test_arr

cap.release()
cv2.destroyAllWindows()
