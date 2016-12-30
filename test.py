import numpy as np
import cv2
import matplotlib.pyplot as plt
import skin_extract as skin
M = 5
h = np.zeros(M)
print h

"""
imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)


Y = imgYCC[:,:,0]
Cb = imgYCC[:,:,2]
Cr = imgYCC[:,:,1]

print type(Y)

indexCb = (Cb >= 80) & (Cb <= 120)
indexCr = (Cr >= 133) & (Cr <= 173)

index = indexCb & indexCr

imnew = np.zeros([350,470], np.uint8)
imnew[index] = 255

print img.shape
print np.sum(indexCb)

#cv2.imshow('detected', imnew)



plt.imshow(indexCb)
plt.pause(0)
plt.imshow(indexCr)
plt.pause(0)
plt.imshow(index)
plt.pause(0)
"""