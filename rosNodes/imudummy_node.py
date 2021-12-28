#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

def sayWhat():
    pub = rospy.Publisher('IMU', Float32MultiArray, queue_size=10)
    rospy.init_node('IMU')
    rospy.loginfo("IMU dummy data was send")
    dataTosend = Float32MultiArray()
    dataTosend.data = [1.1, 333.333, 22.22]
    pub.publish(dataTosend)


if __name__ == '__main__':
	try:
		sayWhat()
	except rospy.ROSInterruptException:
		pass