#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

def imagecb(data):
    # Convert Image message to CV image with blue-green-red color order (bgr8)
    bridge = CvBridge()
    cv2.namedWindow("Image window", 1)
    try:
        img_cv = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
        print("==[CAMERA MANAGER]==", e)

    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    cv2.imshow("Image window", hsv)
    cv2.waitKey(3)


def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/usb_cam/image_raw", Image, imagecb)

    rospy.spin()

if __name__ == '__main__':
    listener()