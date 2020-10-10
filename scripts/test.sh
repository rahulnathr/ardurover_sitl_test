#!/bin/sh

xterm -e "rosrun test_rover rover_rc_controller.py" &
sleep 10
xterm -e "rosbag record -O test1 /mavros/local_position/pose /mavros/vfr_hud __name:=my_test" &
sleep 5
xterm -e "rostopic echo /mavros/local_position/pose"

