#!/usr/bin/env python


import rospy
from std_msgs.msg import Bool
from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes, ObjectCount
from geometry_msgs.msg import Twist 
# from follow_human.msg import Human

rospy.init_node('person_present', anonymous=True) 
move_pub = rospy.Publisher('/person_present', Bool, queue_size=10) 
move_vel = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10) 

def callback(data):
    global move_pub 
    global move_vel
    person_present = False

    for item in data.bounding_boxes:
        if item.Class == "person":
            move_pub.publish(True)
            person_present = True 
            # x = (item.xmin + item.xmax)/2
            # rospy.loginfo("Person's x coordinates: " + str(x))

            # #-----------------------
            # # publish to /cmd_vel
            # move = Twist()
            # #-----------------------

            # if x > 300:
            #     move.angular.z = -0.1
            #     rospy.loginfo("> 300")
            #     move_vel.publish(move) 
            #     rospy.sleep(0.01*x)
            #     move.angular.z = 0
            #     move_vel.publish(move) 

            # if x < 300:
            #     move.angular.z = 0.1
            #     rospy.loginfo("< 300")
            #     move_vel.publish(move) 
            #     rospy.sleep(0.01*x)
            #     move.angular.z = 0
            #     move_vel.publish(move) 

    if person_present == False:
        move_pub.publish(False)


def detect_human():
    bounding_boxes = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, callback) 


if __name__ == "__main__":

    detect_human()

    while not rospy.is_shutdown():
        rospy.spin()
