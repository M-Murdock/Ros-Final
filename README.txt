RUNNING:
--------------
1. ssh onto the turtlebot:

    `ssh turtlebot@<address>`

2. Start up the turtlebot base:

    `roslaunch turtlebot_bringup minimal.launch --screen`

3. Run the launch file with the command: 

    `roslaunch follow_human follow_human.launch` 

4. (Optional) To view the image feed:

    `rosrun image_view image_view image:="/camera/color/image_raw"`


SCRIPTS:
--------------
detect_human.py 
detect_obstacles.py
move_forward.py 


CUSTOM MSG:
--------------
Human.msg 
    ```
    int64 x 
    bool person_present
    ```


COMMANDS:
-------------- 
Copy code onto the turtlebot

    scp -r {path_to_your_pkg} turtlebot@{ip}:~/catkin_ws/src

