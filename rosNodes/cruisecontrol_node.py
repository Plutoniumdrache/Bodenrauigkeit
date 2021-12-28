#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16


def cruiseControl():
    pubSpeed = rospy.Publisher('speed', UInt16, queue_size=10)
    pubAngle = rospy.Publisher('angle', UInt16, queue_size=10)

    rospy.init_node('cruiseControl') # only one init call
    rate = rospy.Rate(10) # 10 Hz
    speed = 90
    angle = 90

    while not rospy.is_shutdown():
        rospy.loginfo("Speed: %s", str(speed))
        pubSpeed.publish(speed)

        rospy.loginfo("Angle: %s", str(angle))
        pubAngle.publish(angle)

        rate.sleep

if __name__ == '__main__':
    try:
        cruiseControl()
    except rospy.ROSInterruptException: # because we are using sleep
        pass
