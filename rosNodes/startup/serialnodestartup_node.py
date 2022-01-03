#!/usr/bin/env python

import rospy
import os

def sayWhat():
    rospy.init_node('startup_Serialnode')
    rospy.loginfo("startup_Serialnode was executed")
    os.system('rosrun rosserial_python serial_node.py /dev/ttyACM0')

if __name__ == '__main__':
	try:
		sayWhat()
	except rospy.ROSInterruptException:
		pass