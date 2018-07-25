# SkypeASL Project
# Task: To capture an image during a live video when there is little to no motion detection
# note to self: white space matters in python 

# import files
import cv2
import numpy as np
import time
# import matplotlib.pyplot as plt
from datetime import datetime


def diffImg(t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)


# threshold that indicates motion detection, can vary for day or night
threshold = 81500

# open camera
cap = cv2.VideoCapture(0)

# to only take one picture a second
timeCheck = datetime.now().strftime('%Ss')

flag = 0
loop_counter = 0
img_counter = 0

# to only take one picture a second
timeCheck = datetime.now().strftime('%Ss')

# infinite loop for video
while (cap.isOpened()):
	ret, frame = cap.read()

	# this just prints out the matrices of the video capture
	print(ret) 
	print(frame)

	# convert to grayscale	
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	
	cv2.imshow('video', frame)
	
	if loop_counter == 0:
		t_minus = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		t = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		t_plus = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	# if there is no movement, the pixel count is below the threshold, then take the picture
	if cv2.countNonZero(diffImg(t_minus, t, t_plus)) <= threshold and timeCheck != datetime.now().strftime('%Ss'):
		img_name = "asl_cam{}.png".format(img_counter)
		cv2.imwrite(img_name, gray)
		print("{} written!".format(img_name))
		img_counter += 1
	
	timeCheck = datetime.now().strftime('%Ss')

	loop_counter += 1

	t_minus = t
	t = t_plus
	t_plus = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	
	# when you press esc it exits cam
	k = cv2.waitKey(1) & 0xff
	if k == 27:
		break

	'''
	#this takes pictures all the time
	else:
		#if <insert some condition of detecting light or pixels lmao>:
		img_name = "asl_cam{}.png".format(img_counter)
		cv2.imwrite(img_name, gray)
		print("{} written!".format(img_name))
		img_counter += 1
	'''

#close camera
cap.release()
cv2.destroyAllWindows()


