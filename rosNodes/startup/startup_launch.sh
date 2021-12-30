#!/bin/bash
source /opt/ros/melodic/setup.bash
#source /home/ubuntu/catkin_ws # macht evt. problemas
export ROS_PACKAGE_PATH=/home/ubuntu/catkin_ws/src/floorpack/launch:$ROS_PACKAGE_PATH
export ROS_PACKAGE_PATH=/home/ubuntu/catkin_ws/src/floorpack:$ROS_PACKAGE_PATH
roslaunch floorpack floorpack.launch