import numpy as np
import cv2
import matplotlib.pyplot as plt
import skin_extract as skin
from eyeDetect import face_loacte, eye_locate, count_black_ratio
from plot_fig import update_line, detect_blink
import setting

face_cascade = cv2.CascadeClassifier('./classifier/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./classifier/haarcascade_eye_tree_eyeglasses.xml')
setting.init()

# limit window size
window_width = 350

# capture input video
#cap = cv2.VideoCapture('./data/0.mov') # capture from file
cap = cv2.VideoCapture(0) # capture from webcam

if cap.isOpened():
    print "Stream Opened Successfuly"
else:
    print "Stream Opened Fail"

face_location = []
eye_location = []

plot_width = 120
plt.axis([0, plot_width,0,1])
plt.suptitle('Real-time Eye blink tracking', fontsize=12)
plt.xlabel('Time')
plt.ylabel('Transformed Value')
plt.ion()

hl, = plt.plot([],[], linewidth=2)
axes = plt.gca()
i = 0

# Moving Average Filter
M = 5
filter_coeff = 1.0/M
s_mem = np.zeros(M)

# main processing loop here
while(cap.isOpened()):
    
    # capture the input image
    ret, img = cap.read()

    
    width = img.shape[1]
    if width > window_width:
        resize_factor = window_width*1.0 / width
        img = cv2.resize(img, (0,0),fx=resize_factor,fy=resize_factor)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find the face location
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

    # crop the eye window
    eye1_gray = roi_gray[e1_y:e1_y+e1_h, e1_x:e1_x+e1_w]
    eye2_gray = roi_gray[e2_y:e2_y+e2_h, e2_x:e2_x+e2_w]
    eye1_color = roi_color[e1_y:e1_y+e1_h, e1_x:e1_x+e1_w]
    eye2_color = roi_color[e2_y:e2_y+e2_h, e2_x:e2_x+e2_w]

    # Transform the window into 1D representitive signal
    black_thresh = 15
    count1 = count_black_ratio( eye1_gray, black_thresh)
    count2 = count_black_ratio( eye2_gray, black_thresh)
    count = count1 + count2
    
    # Moving Average Filter
    s_mem = np.delete(s_mem,0)
    s_mem = np.append(s_mem, count)
    T_value = np.sum(s_mem*filter_coeff)

    # Draw the Results
    update_line(hl, axes, plot_width, i, T_value)
    detect_blink(T_value)
    plt.pause(0.0001)
    i = i + 1

    # Draw the frame
    cv2.rectangle(img,(fx,fy),(fx+fw,fy+fh),(255,0,0),2)
    if T_value < 5:
        cv2.rectangle(roi_color,(e1_x,e1_y),(e1_x+e1_w,e1_y+e1_h),(0,0,255),2)
        cv2.rectangle(roi_color,(e2_x,e2_y),(e2_x+e2_w,e2_y+e2_h),(0,0,255),2)
    else:
        cv2.rectangle(roi_color,(e1_x,e1_y),(e1_x+e1_w,e1_y+e1_h),(0,255,0),2)
        cv2.rectangle(roi_color,(e2_x,e2_y),(e2_x+e2_w,e2_y+e2_h),(0,255,0),2)

    #cv2.imshow('eye1',cv2.resize(eye1_gray, (250, 250)))
    #cv2.imshow('eye2',cv2.resize(eye2_gray, (250, 250)))

    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


cap.release()
cv2.destroyAllWindows()
