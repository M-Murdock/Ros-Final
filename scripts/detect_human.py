#!/usr/bin/env python

# Uses YOLO to detect a person. Publishes to /person_present if one is found.

import rospy
from std_msgs.msg import Bool
from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes, ObjectCount
from follow_human.msg import Human

rospy.init_node('person_present', anonymous=True) 
move_pub = rospy.Publisher('/person_present', Human, queue_size=10) 

def callback(data):
    global move_pub 

    person = Human() 
    person.person_present = False

    for item in data.bounding_boxes:
        # if (item.Class == "person") and (item.probability > 80):
        if (item.Class == "person"):
            person.person_present = True 
            person.x = (item.xmin + item.xmax)/2
            # rospy.loginfo("avg x = " + str((item.xmin + item.xmax)/2))
            # rospy.loginfo("avg y = " + str((item.ymin + item.ymax)/2))
        
    move_pub.publish(person)


def detect_human():
    bounding_boxes = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, callback) 


if __name__ == "__main__":

    detect_human()

    while not rospy.is_shutdown():
        rospy.spin()
