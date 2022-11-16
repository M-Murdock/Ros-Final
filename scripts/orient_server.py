#!/usr/bin/env python

from follow_human.srv import * 
import rospy 

# finds the human's angle relative to the robot
def findAngle(human_pos):
    print(human_pos.pos.x) # placeholder
    return Angle(1.0)

def orient_server():
    #-----------------------
    # initialize the node
    rospy.init_node('orient_server') 

    #-----------------------
    s = rospy.Service('orient', FindAngle, findAngle)
    print("")

    #-----------------------
    rospy.spin()

if __name__ == "__main__":
    orient_server()