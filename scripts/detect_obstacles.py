#!/usr/bin/env python
# license removed for brevity

# Publishes a Bool flag when the turtlebot hits an object 

import rospy
from std_msgs.msg import Bool 
from kobuki_msgs.msg import BumperEvent

# this is called when we get a message from "scan" topic
def obstacle_callback(msg, pub):
    # print("Callback")
    #-----------------------
    if msg.RELEASED == 0:
        pub.publish(True) 

def talker():
    #-----------------------
    # publish to "obstacle"
    pub = rospy.Publisher('obstacle', Bool, queue_size=10)

    #-----------------------
    # subscribe to "scan"
    sub = rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, obstacle_callback, (pub))

    #-----------------------
    # initialize the node
    rospy.init_node('detect_obstacles', anonymous=True) 
    
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass