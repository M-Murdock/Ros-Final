#!/usr/bin/env python
# license removed for brevity

# State machine for controlling robot's actions:
    # move_right/move_left: turns right/left depending on turtlebot's orientation in relation to person
    # wait: turtlebot stops if it hits an obstacle 
    # move_forward: if person is in central view, turtlebot moves forward
    # search: if no person is within view, rotate until the person is found

import rospy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from follow_human.msg import Human


# Globals
#-----------------------
state = "wait"
#-----------------------


# stops if there are obstacles
def obstacle_callback(obstacle_present):
    global state 

    if obstacle_present:
        state = "wait"

# moves forward if a person is detected
def person_present_callback(data):
    global state

    if (data.person_present == True):
        if data.x > 300:
            state = "move_right"
        elif data.x < 200:
            state = "move_left"
        else:
            state = "move_forward"
    else:
        # state = "search"
        state= "search"


def listener():

    global state 

    #-----------------------
    # subscribe to /obstacle
    obstacle = rospy.Subscriber("obstacle", Bool, obstacle_callback)

    #-----------------------
    # subscribe to /person_present
    person_present = rospy.Subscriber("/person_present", Human, person_present_callback)

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
            move.angular.z = 0

        elif state == "move_forward":
            move.linear.x = 0.1 # move forward at constant speed
            move.angular.z = 0

        elif state == "move_right":
            move.linear.x = 0.1
            move.angular.z = -0.1 # turn right, move forward at constant speed

        elif state == "move_left":
            move.linear.x = 0.1
            move.angular.z = 0.1 # turn left, move forward at constant speed
        
        elif state == "search":
            move.linear.x = 0
            move.angular.z = 0.1

        else: # default case: stop moving forward
            move.linear.x = 0
            move.angular.z = 0

        # publish the velocity
        move_pub.publish(move)

        # print("state is: " + state)
        # rospy.loginfo(state)
        rate.sleep()
    #----------------------
    

if __name__ == '__main__':

    #-----------------------
    # initialize the node
    rospy.init_node('move_forward', anonymous=True)
    rate = rospy.Rate(10) # 10hz 

    try:
        state="wait"
        listener()
    except rospy.ROSInterruptException:
        pass