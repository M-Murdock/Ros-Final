#!/usr/bin/env python
# license removed for brevity

# Moves forward until obstacle is detected or the person turns

import rospy
from std_msgs.msg import String, Bool
from follow_human.msg import *
from geometry_msgs.msg import Twist

# called if the human turns
def orientation_callback(data, state):
    print("detected orientation change. turning.")
    state = "orient"

# performs actions depending on whether there are/are not obstacles
def obstacle_callback(data, state):
    if data:
        print("No obstacle detected")
        state = "move forward"
    else:
        print("Detected an obstacle")
        state = "wait"

def talker(state):
    # subscribe to  "orientation" and "obstacle"
    rospy.Subscriber("orientation", Angle, orientation_callback, (state))
    rospy.Subscriber("obstacle", Bool, obstacle_callback, (state))

    #-----------------------
    # initialize the node
    rospy.init_node('move_forward', anonymous=True)
    rate = rospy.Rate(10) # 10hz 

    #-----------------------
    # publish to /cmd_vel
    move_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) 

    #-----------------------
    # create Twist object
    move = Twist()

    move.angular.x = 0
    move.angular.y = 0
    move.angular.z = 0

    move.linear.x = 0
    move.linear.y = 0
    move.linear.z = 0
    #-----------------------
    while not rospy.is_shutdown():
        
        # handle all the states
        if state == "wait":
            move.linear.x = 0 # stop moving forward
            print("waiting") 

        elif state == "orient":
            move.linear.x = 0 # stop moving forward
            # call an action here...
            print("orient") 

        elif state == "move forward":
            move.linear.x = 0.5 # move forward at constant speed
            print("move forward") 

        # publish the velocity
        move_pub.publish(move)


        rospy.loginfo(state)
        rate.sleep()
    #-----------------------

if __name__ == '__main__':
    try:
        state = "move forward"
        talker(state)
    except rospy.ROSInterruptException:
        pass