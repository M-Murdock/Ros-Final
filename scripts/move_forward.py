#!/usr/bin/env python
# license removed for brevity

# Moves forward until obstacle is detected or the person turns

import rospy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist


# Globals
#-----------------------
state = "wait"
#-----------------------


# performs actions depending on whether there are/are not obstacles
def obstacle_callback(obstacle_present):
    global state 
    if obstacle_present:
        state = "wait"
    # else: 
    #     state = "move_forward"


def listener():

    global state 

    #-----------------------
    # subscribe to /obstacle
    obstacle = rospy.Subscriber("obstacle", Bool, obstacle_callback)

    #-----------------------
    # publish to /cmd_vel
    move_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10) 
    move = Twist()
    #-----------------------

    move.angular.x = 0
    move.angular.y = 0
    move.angular.z = 0

    move.linear.x = 0
    move.linear.y = 0
    move.linear.z = 0

    
    while not rospy.is_shutdown():

        # handle all the states
        if state == "wait":
            move.linear.x = 0 # stop moving forward

        elif state == "move_forward":
            move.linear.x = -0.1 # move forward at constant speed
        
        else: # default case: stop moving forward
            move.linear.x = 0

        # publish the velocity
        move_pub.publish(move)

        print("state is: " + state)
        rospy.loginfo(state)
        rate.sleep()
    #----------------------
    

if __name__ == '__main__':

    #-----------------------
    # initialize the node
    rospy.init_node('move_forward', anonymous=True)
    rate = rospy.Rate(10) # 10hz 

    try:
        state="move_forward"
        listener()
    except rospy.ROSInterruptException:
        pass