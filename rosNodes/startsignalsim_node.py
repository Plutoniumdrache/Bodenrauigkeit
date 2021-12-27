#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool

def sayWhat():
    pub = rospy.Publisher('startsignal', Bool, queue_size=10)
    rospy.init_node('startsignal')
    rospy.loginfo("Startsignal was send")
    pub.publish(True)


if __name__ == '__main__':
	try:
		sayWhat()
	except rospy.ROSInterruptException:
		pass