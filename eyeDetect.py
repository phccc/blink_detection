import numpy as np
import cv2

def face_loacte(faces):
    """ locate the one true faces """
    true_face = []
    max_width = 0;
    for (x,y,w,h) in faces:
        if ((w/h) > 1.3) and ((w/h)<0.7):
            continue
        if w > max_width:
            max_width = w;
            true_face = [x,y,w,h]

    return true_face

def eye_locate(eyes):
    """ locate the one true faces """
    find = False
    true_eye = []
    for ii in range(len(eyes)):
        for jj in range(ii+1,len(eyes)):
            eye1 = eyes[ii]
            eye2 = eyes[jj]

            # ratio should match
            size_ratio = eye1[2]/eye2[2]
            if (size_ratio > 1.2) or (size_ratio < 0.8):
                continue

            avg_width = (eye1[2] + eye2[2]) / 2.0
            avg_height = (eye1[3] + eye2[3]) / 2.0

            # y should be close
            y_diff = abs(eye1[1] - eye2[1])
            if (y_diff > avg_height*0.5):
                continue

            # x should seperate
            x_diff = abs(eye1[0] - eye2[0])
            if (x_diff < avg_width) or (x_diff > 3*avg_width):
                continue
            
            # Pass all test, found true eye pair
            true_eye = [eye1, eye2]
            find = True
            break
        if find:
            break
    return true_eye

def count_black(region, thresh):
    rows = len(region)
    cols = len(region[0])
    count = 0
    for ii in range(rows):
        for jj in range(cols):
            if region[ii][jj] < thresh:
                count = count + 1
    return count
