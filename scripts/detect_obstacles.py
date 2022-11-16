#!/usr/bin/env python
# license removed for brevity

# A Node which checks whether an obstacle has been detected. Publishes a Bool flag periodically. 

import rospy
from std_msgs.msg import Bool 
from sensor_msgs.msg import LaserScan

# this is called when we get a message from "scan" topic
def obstacle_callback(msg, pub):
    #-----------------------
    # use "scan" to check whether there's an obstacle within 1 meter
    if msg.ranges[0] < 1: # if so, publish "True" to the topic
        pub.publish(False) 
    else:
        pub.publish(True)

def talker():
    #-----------------------
    # publish to "obstacle"
    pub = rospy.Publisher('obstacle', Bool, queue_size=10)

    #-----------------------
    # subscribe to "scan"
    sub = rospy.Subscriber("/scan", LaserScan, obstacle_callback, (pub))

    #-----------------------
    # initialize the node
    rospy.init_node('detect_obstacles', anonymous=True) 
    
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass