RUNNING:
--------------
Run the launch file with the command: 

    roslaunch follow_human follow_human.launch 


FILES:
--------------
move_forward.py
goal_position_listener.py 
detect_obstacles.py


COMMANDS:
-------------- 
Copy code onto the turtlebot

    scp -r {path_to_your_pkg} turtlebot@{ip}:~/catkin_ws/src


launch the camera 

    roslaunch realbot camera.launch
