#!/usr/bin/env python
# license removed for brevity

# Moves forward until obstacle is detected or the person turns

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
        state = "move_forward"
    else:
        state = "wait"


def listener():

    global state 

    #-----------------------
    # subscribe to /obstacle
    obstacle = rospy.Subscriber("obstacle", Bool, obstacle_callback)

    #-----------------------
    # subscribe to /person_present
    person_present = rospy.Subscriber("/person_present", Human, person_present_callback)
    # person_present = rospy.wait_for_message("/person_present", Bool)
    # if person_present.data == True:
    #     rospy.loginfo("PERSON PRESENT")


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
            move.linear.x = 0.1 # move forward at constant speed
        
        else: # default case: stop moving forward
            move.linear.x = 0

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