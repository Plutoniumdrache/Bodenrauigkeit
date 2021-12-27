#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def sayWhat():
    pub = rospy.Publisher('flurfunk', String, queue_size=10)
    rospy.init_node('flurfunk')
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        moin_str = "Moin Moin"
        rospy.loginfo(moin_str)
        pub.publish(moin_str)
        rate.sleep()


if __name__ == '__main__':
	try:
		sayWhat()
	except rospy.ROSInterruptException:
		pass