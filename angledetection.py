import cv2
import time
import numpy as np
import imutils
from imutils.video import VideoStream
from collections import deque
import math



def takeSecond(elem):
    return elem[0]


def gradient(pt1,pt2):




	return ((pt2[1]-pt1[1])/(pt2[0]-pt1[0]+0.000001))

def getAngle(pointlist):
    pt1,pt2,pt3=pointlist[-3:]
    m1=gradient(pt2,pt1)
    m2=gradient(pt2,pt3)
    angR=math.atan((m2-m1)/(1+(m1*m2)))
    angD=round(math.degrees(angR))
    return angD
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
font = cv2.FONT_HERSHEY_SIMPLEX

pts = deque(maxlen=32)
counter = 0
(dX, dY) = (0, 0)
direction = ""

vs = VideoStream(src=0).start()
def nothing(*arg):
        pass
greenLower = (0, 0, 255)
greenUpper = (92, 17, 255)

# icol = (0, 0, 0, 255, 255, 255)
# cv2.namedWindow('colorTest')
# cv2.createTrackbar('lowHue', 'colorTest', icol[0], 255, nothing)
# cv2.createTrackbar('lowSat', 'colorTest', icol[1], 255, nothing)
# cv2.createTrackbar('lowVal', 'colorTest', icol[2], 255, nothing)
# # Higher range colour sliders.
# cv2.createTrackbar('highHue', 'colorTest', icol[3], 255, nothing)
# cv2.createTrackbar('highSat', 'colorTest', icol[4], 255, nothing)
# cv2.createTrackbar('highVal', 'colorTest', icol[5], 255, nothing)

while True:
	# grab the current frame
	frame = vs.read()
	frame=cv2.flip(frame, 1)
	# cv2.namedWindow('colorTest')
	# lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
	# lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
	# lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')
	# highHue = cv2.getTrackbarPos('highHue', 'colorTest')
	# highSat = cv2.getTrackbarPos('highSat', 'colorTest')
	# highVal = cv2.getTrackbarPos('highVal', 'colorTest')
	# greenLower = (lowHue, lowSat, lowVal)
	# greenUpper = (highHue, highSat, highVal)
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
    # resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	cv2.imshow("Blur",blurred)

	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	cv2.imshow("hsv", hsv)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cv2.imshow("mask", mask)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	center = None
	center_list=[]
	abc=sorted(cnts,key=cv2.contourArea,reverse=True)
    # only proceed if at least one contour was found
	if len(abc) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		#abc=sorted(zip(cnts), reverse=True)[:3]
		##c = max(cnts, key=cv2.contourArea)

		for i in (abc):
			((x, y), radius) = cv2.minEnclosingCircle(i)
			M = cv2.moments(i)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
						   (0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				center_list.append(center)
	#	print("us: "+str(center_list))
		center_list.sort(key=takeSecond)
	#	print("srt:"+str(center_list))
		if(len(center_list)>1):
			for i in range(len(center_list)-1):
				cv2.line(frame,(center_list[i]),center_list[i+1],(0,255,0),thickness=3)
		if(len(center_list)==3):
			angle=getAngle(center_list)
			cv2.putText(frame,str(angle),center_list[1],font,1,(0,0,255),3,cv2.LINE_AA)

	# update the points queue


	cv2.imshow('frame',frame)
	key=cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

vs.stop()
vs.release()
cv2.destroyAllWindows()

