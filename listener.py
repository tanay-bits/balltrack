#!/usr/bin/env python

import rospy
import cv2
import cv2.cv
import numpy as np
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def imagecb(data):
    # Convert Image message to CV image with blue-green-red color order (bgr8)
    bridge = CvBridge()
    cv2.namedWindow("image window")
    try:
        img_cv = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
        print("==[CAMERA MANAGER]==", e)

    
    # img_cv = cv2.medianBlur(img_cv,5)    
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    lower_red = np.array([-5,170,50])
    upper_red = np.array([5,255,255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    res = cv2.bitwise_and(img_cv,img_cv, mask=mask)

    resgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(resgray,cv2.cv.CV_HOUGH_GRADIENT,1.2,550,param1=50,param2=30,minRadius=100,maxRadius=300)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		    cv2.circle(res, (x, y), r, (0, 255, 0), 4)
		    cv2.rectangle(res, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


   

    cv2.imshow("image window", res)
    cv2.waitKey(5)


def listener():
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/usb_cam/image_raw", Image, imagecb)

    rospy.spin()

if __name__ == '__main__':
    listener()