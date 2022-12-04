#!/usr/bin/env python

import rospy 
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError 
import imutils

# Globals
#-----------------------
# Initialize the CvBridge class
bridge = CvBridge()

#-----------------------
# initialize the node
rospy.init_node('cv', anonymous=True) 




def save_image(img):
    # rospy.loginfo("showing image")
    cv2.imwrite("img.png", img)


def cv(img_msg):
    # rospy.loginfo(img_msg.header)

    global bridge
    #-----------------------
    # Try to convert the ROS Image message to a CV2 Image
    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # Show the converted image
    save_image(cv_image)


if __name__ == "__main__":

    # Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
    sub_image = rospy.Subscriber("/camera/color/image_raw", Image, cv) 


    # Initializing the HOG person
    # detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    image = cv2.imread('img.png')


    # Resizing the Image
    image = imutils.resize(image, width=min(400, image.shape[1]))
    
    (regions, _) = hog.detectMultiScale(image, winStride=(4,4),padding=(4,4),scale=1.05)
   
    for (x, y, w, h) in regions:
        rospy.loginfo("human detected")
        cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2)
        save_image(image)
    
    # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
    while not rospy.is_shutdown():
        rospy.spin()